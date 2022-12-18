<script>
    import {onMount} from "svelte";
    import axios from "axios";
    import {generateName, timeAgo, randomSentence} from "./textGeneration.js";

    import Loading from "./Loading.svelte";
    import Sentiment from "./Sentiment.svelte";
    import Summary from "./Summary.svelte";
    import Verdict from "./Verdict.svelte";

    export let verdict;
    export let url;
    let fullUrl = `https://www.reddit.com/r/AmItheAsshole/comments/${url}`

    let analyse;

    const snuLocation = new URL('./snu_color.png', import.meta.url).href;

    let loading = true;
    let post = {comments: [], body: "", title: ""};
    onMount(async () => {
        const options = {
            params: {url},
            headers: {"content-type": "application/json"}
        }
        const data = await axios.get("http://127.0.0.1:5000/post", options);
        post = data.data;
        loading = false;
    });
</script>

{#if loading}
    <div class="mt-12">
        <Loading/>
    </div>
{:else}
    <div class="view">
        <div class="post">
            <div class="post-header">
                <div class="post-description">
                    <span class="post-description-subreddit">r/AmItheAsshole</span>&nbsp;• Posted by
                    u/{generateName(post.body)} {timeAgo(post.timestamp)}
                </div>
                <a class="post-title" href={fullUrl} target="_blank" rel="noreferrer">
                    { post.title }
                </a>
            </div>
            <Verdict verdict={verdict}/>

            <div class="post-body">
                {@html post.body }
            </div>

            <hr/>

            <div class="post-comments">
                {#each post.comments as comment}
                    <div class="comment">
                        <div class="comment-header">
                            <img src={snuLocation} class="avatar"
                                 style={`filter: hue-rotate(${Math.floor(Math.random()*360)}deg)`}/>
                            <div class="comment-header-text">
                                <div class="comment-author">
                                    {generateName(comment.body)}
                                </div>
                                <div class="comment-time">
                                    · {timeAgo(comment.timestamp)}
                                </div>
                                {#if comment.verdict}
                                    <Verdict verdict={comment.verdict}/>
                                {/if}

                            </div>
                        </div>

                        <div class="comment-body">
                            {@html comment.body}
                            <div class="comment-upvotes">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 0 1010 1000">
                                    <g transform="matrix(1 0 0 -1 0 1000)">
                                        <path d="M650 44h-300q-23 0 -39.5 16.5t-16.5 39.5v344h-188q-16 0 -30 9t-21 24.5t-4.5 32t13.5 28.5l394 437q17 18 42 18t42 -18l394 -437q11 -12 13.5 -28.5t-4 -32t-20.5 -24.5t-31 -9h-188v-344q0 -23 -16.5 -39.5t-39.5 -16.5zM356 106h288v400l236 1l-380 421l-380 -421h236v-401zM505 933z"/>
                                    </g>
                                </svg>
                                {comment.score}
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 0 1010 1000">
                                    <g transform="matrix(1 0 0 -1 0 1000)">
                                        <path d="M500 6q-25 0 -42 19l-394 437q-11 12 -13.5 28.5t4 32t20.5 24.5t31 9h188v344q0 23 16.5 39.5t39.5 16.5h300q23 0 39.5 -16.5t16.5 -39.5v-344h188q16 0 30 -9t21 -24.5t4.5 -32t-13.5 -28.5l-394 -437q-17 -19 -42 -19zM495 67zM120 493l380 -421l380 421h-236v401h-288v-400z"/>
                                    </g>
                                </svg>
                            </div>
                        </div>
                    </div>

                {/each}
            </div>
        </div>
        <div class="analysis">
            <Summary url={url}></Summary>
            <Sentiment body={post.body}>Judge this post</Sentiment>
        </div>
    </div>

{/if}

<style>
    .post {
        display: flex;
        margin: 16px;

        flex-direction: column;
        align-items: start;
        background-color: var(--secondary-background);
        border-radius: 4px;
        border: 1px solid var(--border-color);
        padding: 16px;
        transition: all 0.2s ease-in-out;
        gap: 4px;
    }

    .post-header {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }


    .post-title {
        color: var(--text-color);
        text-decoration: none;

        font-family: IBM Plex Sans Medium, Arial, sans-serif;
        font-size: 20px;
        font-weight: 600;
    }

    .post-description {
        display: flex;
        align-items: center;

        font-family: IBM Plex Sans, Arial, sans-serif;
        font-size: 12px;
        color: var(--text-fainter-color);
    }

    .post-description-subreddit {
        color: var(--text-color);
        font-weight: 700;
    }

    .post-body {
        margin-top: 8px;
        color: var(--text-faint-color);
        font-family: Noto Sans, Arial, sans-serif;
        font-size: 14px;
        font-weight: 400;
        line-height: 21px;
    }

    .view {
        display: flex;
        flex-direction: row;
    }

    .analysis {
        display: flex;
        flex-direction: column;
        gap: 16px;
        margin: 16px;
    }

    .analysis {
        background-color: var(--secondary-background);
        border-radius: 4px;
        padding: 16px;
        margin: 16px;
        border: 1px solid var(--border-color);

        display: flex;
        height: min-content;
        min-height: 250px;
        min-width: 40%;

        flex-direction: column;
        gap: 16px;
    }

    .avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        margin-right: 8px;
        z-index: 0;
    }

    .post-comments {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .comment {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .comment-header {
        display: flex;
        align-items: center;
    }

    .comment-header-text {
        display: flex;
    }

    .comment-body {
        display: block;
        margin-left: 12px;
        padding-left: 16px;
        border-left: 2px solid var(--faint-border-color);

        font-family: Noto Sans, Arial, sans-serif;
        font-size: 14px;
        font-weight: 400;
    }

    .comment-header-text {
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .comment-author {
        color: var(--text-color);
        font-family: IBM Plex Sans Medium, Arial, sans-serif;
        font-size: 12px;
        font-weight: 600;
    }

    .comment-time {
        color: var(--text-fainter-color);
        font-family: Noto Sans, Arial, sans-serif;
        font-size: 12px;
        font-weight: 400;
    }

    .comment-upvotes {
        display: flex;
        align-items: center;
        gap: 6px;
        font-family: IBM Plex Sans, Arial, sans-serif;
        font-size: 12px;
        font-weight: 700;
    }

    .comment-upvotes svg {
        fill: var(--icon-color);
        width: 20px;
        height: 20px;
    }

</style>