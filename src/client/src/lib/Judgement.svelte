<script>
    import Sentiment from "./Sentiment.svelte";

    let body;
</script>

<div>
    <textarea class="judgement-area" placeholder="Describe your grievings here..." bind:value={body}/>
    <Sentiment {body}/>
</div>

<style>
    .judgement-area {
        border-radius: 16px;
        margin: 16px;
        padding: 16px;
        outline: 1px solid var(--border-color);
        resize: none;

        height: 500px;
        width: 500px;

        font-family: IBM Plex Sans, Arial, sans-serif;
        font-size: 16px;

    }

    .judgement-area:focus {
        outline: 2px solid var(--border-color-hover);
    }

</style>
