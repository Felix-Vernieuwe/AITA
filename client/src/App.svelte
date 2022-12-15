<script>
    import axios from "axios";
    
    import Post from "./lib/Post.svelte";
    import Loading from "./lib/Loading.svelte";
    import Analysis from "./lib/Analysis.svelte";
    import { PENDING, LOADING, SEARCH_RESULTS, ANALYSING } from "./lib/status.js";

    let status = PENDING;
    let posts = [];
    let searchTerm;
    function query()
    {
        status = LOADING;
        const options = {
            params: { query: searchTerm },
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
        selectedPost = event.detail.url;
        status = ANALYSING;
    }
</script>

<main class="w-screen h-screen flex flex-col text-slate-400 bg-slate-800 overflow-hidden">
    <div class="w-full">
        <div class="mx-auto w-1/3">
            <form on:submit|preventDefault={query}>
                <input type="text" placeholder="Search for posts..." bind:value={searchTerm}
                    class="my-2 p-4 w-full rounded-md border border-slate-400 bg-slate-700">
            </form>
        </div>
    </div>
    <div class="w-full grow overflow-hidden">
        {#if status === LOADING}
            <Loading/>
        {:else if status === SEARCH_RESULTS}
            <div class="overflow-scroll space-y-2">
                {#each posts as { title, url }}
                    <Post {title} {url} on:selected={selectPost}></Post>
                {/each}
            </div>
        {:else if status === ANALYSING}
            <Analysis url={selectedPost}></Analysis>
        {/if}
    </div>
</main>