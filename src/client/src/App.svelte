<script>
    import axios from "axios";
    
    import Post from "./lib/Post.svelte";
    import Loading from "./lib/Loading.svelte";
    import Analysis from "./lib/Analysis.svelte";
    import Judgement from "./lib/Judgement.svelte";
    import { PENDING, LOADING, SEARCH_RESULTS, ANALYSING, JUDGING } from "./lib/status.js";

    let fieldTerms = ["title", "body"];
    let fields = fieldTerms.reduce((object, term) => ({ ...object, [term]: false}), {});
    fields.title = true;

    let capitalise = string => string[0].toUpperCase() + string.slice(1);

    let status = PENDING;
    let posts = [];
    let searchTerm;
    function query()
    {
        status = LOADING;
        const options = {
            params: { query: searchTerm, filters: Object.keys(fields).filter(field => fields[field]).join(",") },
            headers: { "content-type": "application/json" }
        }
        axios.get("http://127.0.0.1:5000/posts", options)
            .then(data => {
                status = SEARCH_RESULTS;
                posts = data.data.posts;
            });
    }

    let selectedPost = undefined;
    function selectPost(event)
    {
        searchTerm = undefined;
        selectedPost = event.detail;
        status = ANALYSING;
    }
</script>

<main class="w-screen h-screen flex flex-col text-slate-400 bg-slate-800 overflow-hidden">
    <div class="w-full">
        <div class="flex justify-center">
            <div class="p-2 absolute left-0 text-xl">
                r/AmITheAsshole Analyser
            </div>
            <div class="my-2 w-1/3 relative">
                <form on:submit|preventDefault={query}>
                    <input type="text" placeholder="Search for posts..." bind:value={searchTerm}
                        class="p-4 w-full rounded-md border border-slate-400 bg-slate-700">
                </form>
                <div class="ml-2 my-2 absolute left-full top-0 inline-flex rounded-md border
                           border-slate-400 divide-x divide-slate-400 overflow-hidden">
                    {#each Object.keys(fields) as field}
                        <button class="p-2 cursor-pointer text-slate-200" class:bg-sky-700={fields[field]}
                            on:click|preventDefault={() => fields[field] = !fields[field]}>
                            { capitalise(field) }
                        </button>
                    {/each}
                </div>
            </div>
            {#if status !== JUDGING}
                <button class="m-2 p-2 absolute right-0 rounded-md bg-sky-700 text-slate-200"
                        on:click={() => status = JUDGING}>
                    Judge Me!
                </button>
            {/if}
        </div>
    </div>
    <div class="w-full grow overflow-hidden">
        {#if status === LOADING}
            <Loading/>
        {:else if status === SEARCH_RESULTS}
            <div class="overflow-scroll space-y-2">
                {#each posts as { title, url, verdict }}
                    <Post {title} {url} {verdict} on:selected={selectPost}></Post>
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
</main>