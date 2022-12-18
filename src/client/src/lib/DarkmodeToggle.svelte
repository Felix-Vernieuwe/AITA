<script>
    export let darkmode = false;


</script>

<label class="darkmode-toggle-wrapper">
    <div class="darkmode-toggle" class:darkmode-toggle-enabled={darkmode}>
        <div class="darkmode-toggle-icons">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3a6.364 6.364 0 0 0 9 9 9 9 0 1 1-9-9Z"></path>
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="4"></circle>
                <path d="M12 2v2"></path>
                <path d="M12 20v2"></path>
                <path d="m4.93 4.93 1.41 1.41"></path>
                <path d="m17.66 17.66 1.41 1.41"></path>
                <path d="M2 12h2"></path>
                <path d="M20 12h2"></path>
                <path d="m6.34 17.66-1.41 1.41"></path>
                <path d="m19.07 4.93-1.41 1.41"></path>
            </svg>
        </div>
        <input type="checkbox" bind:checked={darkmode}/>
    </div>
</label>

<style>
    .darkmode-toggle-wrapper {
        bottom: 16px;
        right: 16px;
        float: right;

        display: block;
    }

    .darkmode-toggle {
        position: relative;

        height: 32px;
        width: 64px;

        background: var(--secondary-background);
        margin: auto;


        cursor: pointer;

        border-radius: 50px;

        border: 0;
        background-color: var(--primary-accent-color);
        color: var(--text-complement-accent-color);
    }

    .darkmode-toggle::before {
        content: "";
        display: block;
        height: 26px;
        width: 26px;
        top: 3px;
        left: 4px;


        border-radius: 30px;
        background-color: #fff;
        position: absolute;
        z-index: 2;
        transform: translate(0);
        transition: transform 0.2s ease;
    }

    .darkmode-toggle-enabled::before {
        transform: translate(30px);
    }

    .darkmode-toggle input {
        position: absolute;
        top: 0;
        opacity: 0;
    }

    .darkmode-toggle-icons {
        padding: 4px 5px;

        position: relative;
        display: flex;

        justify-content: space-between;
        align-items: center;
    }

    .darkmode-toggle-icons > svg {
        z-index: 0;
        fill: var(--text-complement-accent-color);
    }

</style>