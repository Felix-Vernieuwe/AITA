<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let title;
    export let url;

    // let limit = 400;
    // let truncatedBody = body.slice(0, limit);
</script>

<div class="mx-auto w-1/2 bg-slate-900">
    <button class="w-full h-full p-2 text-slate-400 rounded-md border border-slate-400" on:click={() => dispatch('selected', { url })}>
        <div class="text-xl">
            {title}
        </div>
        <!-- <div>
            {truncatedBody}{body.length < limit ? "" : "..."}
        </div> -->
    </button>
</div>