<script>
    export let text;
    export let value;
    export let min = 0;
    export let max = 100;

    $: subDivision = Math.max(0, Math.min(9, 10 - Math.floor((value - min) / ((max - min) / 10))));
</script>

<span class={`analysis-percentage gradient-${subDivision}`}>{text}</span>

<style>
    .gradient-0 {
        background: linear-gradient(to right, #57bb8a 0%, #73b87e 100%);
    }

    .gradient-1 {
        background: linear-gradient(to right, #73b87e 0%, #94bd77 100%);
    }

    .gradient-2 {
        background: linear-gradient(to right, #94bd77 0%, #b0be6e 100%);
    }

    .gradient-3 {
        background: linear-gradient(to right, #b0be6e 0%, #d4c86a 100%);
    }

    .gradient-4 {
        background: linear-gradient(to right, #d4c86a 0%, #f5ce62 100%);
    }

    .gradient-5 {
        background: linear-gradient(to right, #f5ce62 0%, #e9b861 100%);
    }

    .gradient-6 {
        background: linear-gradient(to right, #e9b861 0%, #ecac67 100%);
    }

    .gradient-7 {
        background: linear-gradient(to right, #ecac67 0%, #e79a69 100%);
    }

    .gradient-8 {
        background: linear-gradient(to right, #e79a69 0%, #e2886c 100%);
    }

    .gradient-9 {
        background: linear-gradient(to right, #e2886c 0%, #dd776e 100%);
    }

    .analysis-percentage {
        color: var(--text-complement-accent-color);
        font-family: IBM Plex Sans, Arial, sans-serif;
        font-size: 13px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 25px;
    }
</style>