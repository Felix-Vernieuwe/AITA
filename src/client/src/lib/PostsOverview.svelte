<script>
    import {LOADING, SEARCH_RESULTS} from "./status.js";
    import {navigate} from "svelte-routing";
    import axios from "axios";

    import Post from "./Post.svelte";
    import Loading from "./Loading.svelte";
    import {onMount} from "svelte";

    export let query = "";

    let nextPage = 1;
    let newQuery = true;

    let posts = [];
    let status = LOADING;

    let fieldTerms = ["title", "body"];
    let fields = fieldTerms.reduce((object, term) => ({...object, [term]: false}), {});
    fields.title = true;

    $: query, newQuery = true, fetchPosts(), console.log("query changed", query);

    async function fetchPosts() {
        if (newQuery) {
            nextPage = 1;
            posts = [];
        }

        if (nextPage) {

            const options = {
                params: {
                    query: query,
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
</script>

{#if posts.length}
    <div class="posts-grid">
        {#each posts as {title, url, verdict, timestamp}}
            <Post {title} {url} {verdict} {timestamp} on:selected={() => navigate(`/post/${url}`)}/>
        {/each}
    </div>

    {#if nextPage}
        {#if status === LOADING}
            <Loading/>
        {:else}
            <button class="post-loading-button" on:click={async () => await fetchPosts()}>
                Load more posts...
            </button>
        {/if}
    {/if}
{:else if !newQuery}
    <span class="no-posts">
        Oops! No posts were found...
    </span>
{/if}