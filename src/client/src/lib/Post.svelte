<script>
    import {createEventDispatcher} from "svelte";
    import {generateName, timeAgo, randomSentence} from "./textGeneration.js";
    import Verdict from "./Verdict.svelte";

    const dispatch = createEventDispatcher();

    export let title;
    export let url;
    export let verdict;
    export let timestamp;


    const display_name = generateName(title);
    const display_timestamp = timeAgo(timestamp);
    const display_sentence = randomSentence(title);

</script>

<div class="post post-contents" on:click={() => dispatch('selected', { url, verdict })}>
    <div class="post-header">
        <div class="post-description">
            Posted by u/{display_name}   {display_timestamp}
        </div>

        <Verdict {verdict}/> {title}

    </div>

    <div class="post-placeholder">
        {display_sentence}
    </div>
</div>

<style>
    .post-contents {
        display: flex;
        flex-direction: column;
        align-items: start;

        transition: all 0.2s ease-in-out;
        gap: 4px;

        font-family: IBM Plex Sans Medium, Arial, sans-serif;
        font-size: 18px;
        font-weight: 600;
    }

    .post-header {
        display: block;
        min-height: 40px;
        color: var(--text-color);
    }

    .post:hover {
        outline: 1px solid var(--border-color-hover);
    }

    .post-description {
        font-size: 12px;
        font-weight: 400;
        margin-bottom: 4px;
        color: var(--text-fainter-color);
        font-family: IBM Plex Sans Medium, Arial, sans-serif;
    }

    .post-placeholder {
        font-family: 'Flow Circular', cursive;
        font-weight: normal;
        font-size: 18px;

        line-height: 0.9;
        color: #424242;
    }

</style>