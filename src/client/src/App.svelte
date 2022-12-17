<script>
    import axios from "axios";

    import Post from "./lib/Post.svelte";
    import Loading from "./lib/Loading.svelte";
    import Analysis from "./lib/Analysis.svelte";
    import Judgement from "./lib/Judgement.svelte";
    import {PENDING, LOADING, SEARCH_RESULTS, ANALYSING, JUDGING} from "./lib/status.js";

    let fieldTerms = ["title", "body"];
    let fields = fieldTerms.reduce((object, term) => ({...object, [term]: false}), {});
    fields.title = true;

    let capitalise = string => string[0].toUpperCase() + string.slice(1);

    let status = PENDING;
    let posts = [];
    let searchTerm;

    function query() {
        status = LOADING;
        const options = {
            params: {query: searchTerm, filters: Object.keys(fields).filter(field => fields[field]).join(",")},
            headers: {"content-type": "application/json"}
        }
        axios.get("http://127.0.0.1:5000/posts", options)
            .then(data => {
                status = SEARCH_RESULTS;
                posts = data.data.posts;
                console.log(posts);
            });
    }

    let selectedPost = undefined;

    function selectPost(event) {
        searchTerm = undefined;
        selectedPost = event.detail;
        status = ANALYSING;
    }

    let darkmode = false;
    $: document.body.classList.toggle("dark-theme", darkmode);

    let input_field = null;

</script>

<div class="main-screen">
    <div class="top-column">
        <div class="title-bar">
            r/<span class="title-bar-highlighted">A</span>m<span class="title-bar-highlighted">I</span><span
                class="title-bar-highlighted">T</span>he<span class="title-bar-highlighted">A</span>sshole Analyser
        </div>
        <div class="search-bar">
            <form on:submit|preventDefault={query}>
                <div class="search-input" on:click={() => input_field.focus()}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
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
                        { capitalise(field) }
                    </button>
                {/each}
            </div>
        </div>
        <button class="judge-button"
                on:click={() => status = JUDGING}>
            {status !== JUDGING ? "Judge Me!" : "Back to search"}
        </button>
    </div>
    <div class="bottom-column">
        {#if status === LOADING}
            <Loading/>
        {:else if status === SEARCH_RESULTS}
            <div class="posts-grid">
                {#each posts as {title, url, verdict, timestamp}}
                    <Post {title} {url} {verdict} {timestamp} on:selected={selectPost}></Post>
                {/each}
            </div>
        {:else if status === ANALYSING}
            <Analysis {...selectedPost}></Analysis>
        {:else if status === JUDGING}
            <div class="mx-auto w-1/2">
                <Judgement></Judgement>
            </div>
        {/if}
    </div>
</div>

<label class="darkmode-toggle-wrapper">
    <div class="darkmode-toggle" class:darkmode-toggle-enabled={darkmode}>
        <div class="darkmode-toggle-icons">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3a6.364 6.364 0 0 0 9 9 9 9 0 1 1-9-9Z"></path>
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="4"></circle>
                <path d="M12 2v2"></path>
                <path d="M12 20v2"></path>
                <path d="m4.93 4.93 1.41 1.41"></path>
                <path d="m17.66 17.66 1.41 1.41"></path>
                <path d="M2 12h2"></path>
                <path d="M20 12h2"></path>
                <path d="m6.34 17.66-1.41 1.41"></path>
                <path d="m19.07 4.93-1.41 1.41"></path>
            </svg>
        </div>
        <input type="checkbox" bind:checked={darkmode}/>
    </div>
</label>