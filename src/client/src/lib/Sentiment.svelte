<script>
    import axios from "axios";

    export let body;

    let methods = ["BERT", "MNB"];
    let method;

    let sentiment;
    function analyse()
    {
        if (body !== undefined)
        {
            const options = {
                params: { body, method },
                headers: { "content-type": "application/json" }
            }
            axios.get("http://127.0.0.1:5000/sentiment", options)
                .then(data => {
                    sentiment = data.data;
                });
        }
    }

    function message(nta)
    {
        if (nta) return "not the asshole";
        else     return "the asshole";
    }
</script>

<div class="flex text-right text-lg">
    <button class="p-1.5 h-fit flex-none rounded-md bg-sky-700 text-slate-200" on:click={analyse}>
        <slot></slot>
    </button>
    <select class="p-2 ml-2 h-fit rounded-md bg-sky-700 text-slate-200" bind:value={method}>
        {#each methods as method}
            <option value={method}>{ method }</option>
        {/each}
    </select>
    {#if sentiment !== undefined}
        <div class="p-1.5 grow text-lg">
            Our AI model considers the OP of this post to be { message(sentiment.nta) }, with { sentiment.certainty }% certainty
        </div>
    {/if}
</div>