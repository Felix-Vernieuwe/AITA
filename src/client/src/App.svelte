<script>
    import axios from "axios";

    import Post from "./lib/Post.svelte";
    import Loading from "./lib/Loading.svelte";
    import Analysis from "./lib/Analysis.svelte";
    import Judgement from "./lib/Judgement.svelte";
    import {PENDING, LOADING, SEARCH_RESULTS, ANALYSING, JUDGING} from "./lib/status.js";
    import DarkmodeToggle from "./lib/DarkmodeToggle.svelte";

    let fieldTerms = ["title", "body"];
    let fields = fieldTerms.reduce((object, term) => ({...object, [term]: false}), {});
    fields.title = true;

    let status = PENDING;
    let posts = [];
    let searchTerm;
    let nextPage = 0;
    let newQuery = true;

    let mode = "search";

    $: searchTerm, newQuery = true;

    async function query() {
        mode = "search";

        if (newQuery)
            nextPage = 1;

        if (nextPage) {
            status = LOADING;

            const options = {
                params: {
                    query: searchTerm,
                    filters: Object.keys(fields).filter(field => fields[field]).join(","),
                    page: nextPage || 1
                },
                headers: {"content-type": "application/json"}
            }
            const data = await axios.get("http://127.0.0.1:5000/posts", options);

            status = SEARCH_RESULTS;
            if (data.data.nextpage) {
                posts = [...posts, ...data.data.posts];
                nextPage = data.data.nextpage;
            } else {
                posts = data.data.posts;
                nextPage = 0;
            }
            newQuery = false;
        }
    }

    let selectedPost = undefined;

    function selectPost(event) {
        searchTerm = undefined;
        selectedPost = event.detail;
        status = ANALYSING;
        mode = "analysis";
    }

    let darkmode = false;
    $: document.body.classList.toggle("dark-theme", darkmode);

    let input_field = null;

</script>

<div class="main-screen">
    <div class="top-column">
        <div class="title-bar">
            r/<span class="title-bar-highlighted">A</span>m<span class="title-bar-highlighted">I</span><span
                class="title-bar-highlighted">T</span>he<span class="title-bar-highlighted">A</span>nalyser
        </div>
        <div class="search-bar">
            <form on:submit|preventDefault={query}>
                <div class="search-input" on:click={() => input_field.focus()}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                         class="search-color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    >
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input bind:this={input_field} type="text" placeholder="Search for posts..."
                           bind:value={searchTerm}/>
                </div>

            </form>
            <div class="search-buttons">
                {#each Object.keys(fields) as field}
                    <button class="search-button" class:search-button-active={fields[field]}
                            on:click|preventDefault={() => fields[field] = !fields[field]}>
                        { field }
                    </button>
                {/each}
            </div>
        </div>
        <div class="top-right-bar">
            <button class="judge-button"
                    on:click={() => status = JUDGING}>
                {status !== JUDGING ? "Judge Me!" : "Back to search"}
            </button>
            <DarkmodeToggle bind:darkmode/>
        </div>
    </div>
    <div class="bottom-column">
        {#if mode === "search"}
            {#if posts.length}
                <div class="posts-grid">
                    {#each posts as {title, url, verdict, timestamp}}
                        <Post {title} {url} {verdict} {timestamp} on:selected={selectPost}></Post>
                    {/each}
                </div>

                {#if nextPage}
                    {#if status === LOADING}
                        <Loading/>
                    {:else}
                        <button class="post-loading-button" on:click={async () => await query()}>
                            Load more posts...
                        </button>
                    {/if}
                {/if}
            {:else if !newQuery}
                <span class="no-posts">
                    Oops! No posts were found...
                </span>
            {/if}
        {:else if mode === "analysis"}
            <Analysis {...selectedPost} on:back={() => mode = "search"}/>
        {:else if mode === "judgement"}
            <Judgement/>
        {/if}
    </div>
</div>