<script>
    import axios from "axios";

    import Sentiment from "./Sentiment.svelte";

    let body;
    let sentiment;
    function judge()
    {
        const options = {
            params: { body },
            headers: { "content-type": "application/json" }
        }
        axios.get("http://127.0.0.1:5000/sentiment", options)
            .then(data => {
                sentiment = data.data;
            });
    }
</script>

<div>
    <textarea class="mt-2 p-2 w-full h-96 focus:outline-none focus:ring focus:ring-slate-400 resize-none rounded-md bg-slate-900 text-slate-400"
            placeholder="Describe your torments here..." bind:value={body}></textarea>
    <div class="flex">
        <button class="p-2 rounded-md bg-sky-700 text-slate-200" on:click={judge}>
            Judge me!
        </button>
        {#if sentiment !== undefined}
            <div class="grow">
                <Sentiment {sentiment}></Sentiment>
            </div>
        {/if}
    </div>
</div>