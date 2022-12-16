<script>
    import { onMount } from "svelte";
    import axios from "axios";

    import Loading from "./Loading.svelte";
    import Sentiment from "./Sentiment.svelte";
    import Summary from "./Summary.svelte";

    export let url;
    let fullUrl = `https://www.reddit.com/r/AmItheAsshole/comments/${url}`

    let analyse;

    let loading = true;
    let post = { comments: [], body: "", title: "" };
    onMount(() => {
        const options = {
            params: { url },
            headers: { "content-type": "application/json" }
        }
        axios.get("http://127.0.0.1:5000/post", options)
            .then(data => {
                post = data.data;
                loading = false;
            });
        });
</script>

{#if loading}
    <div class="mt-12">
        <Loading/>
    </div>
{:else}
    <div class="p-2 pb-0 h-full grid grid-cols-2 gap-2">
        <div class="overflow-scroll">
            <div class="h-96 bg-slate-900 relative rounded-md border-2 border-slate-400 overflow-scroll">
                <a class="p-2 block bg-inherit sticky top-0 border-b-2 border-slate-400 text-xl"
                    href={fullUrl} target="_blank" rel="noreferrer">
                    { post.title }
                </a>
                <div class="p-2">
                    {@html post.body }
                </div>
            </div>
            <div>
                <Summary url={url}></Summary>
            </div>
            <div class="my-2">
                <Sentiment body={post.body}>Judge this post</Sentiment>
            </div>
        </div>
        <div class="overflow-scroll">
            {#each post.comments as comment}
                <div class="mb-2 p-2 bg-slate-900 rounded-md border-2 border-slate-400">
                    {@html comment}
                </div>
            {/each}
        </div>
    </div>
{/if}