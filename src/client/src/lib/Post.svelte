<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let title;
    export let url;
    export let verdict;
    export let timestamp;


    const display_verdict = {
        "not the asshole": "Not the A-hole",
        "no assholes here": "No A-holes here",
        "everyone sucks": "Everyone Sucks",
        "asshole": "Asshole",
        "info": "INFO"
    }

    const class_verdict = {
        "not the asshole": "post-nta",
        "no assholes here": "post-nah",
        "everyone sucks": "post-esh",
        "asshole": "post-yta",
        "info": "post-info"
    }


    function TitleCase(sentence) {
        return sentence
            .toLowerCase()
            .split(" ")
            .map((word) => word[0].toUpperCase() + word.slice(1))
            .join(" ");
    }

    function selectRandomly(list) {
        return list[Math.floor(Math.random() * list.length)];
    }

    function selectRandomWordsFromTitle() {
        // Filter words like 'AITA' and 'Update' from the title
        const filter_words = [
            'aita', 'update', 'am', 'i', 'the', 'asshole', 'for', 'my', "i'm", 'a',
            'she'
        ]
        let words = title.split(' ');
        words = words
            .map(word => word.toLowerCase().replace(/[^\w\s]/gi, ''))
            .filter(word => !filter_words.includes(word));

        // Select two to four random words, make sure length is maximum 20 characters
        let selected_words = [];
        let selected_words_length = 0;
        while (selected_words_length < 20 && selected_words.length < 4) {
            let random_word = selectRandomly(words);
            selected_words.push(random_word);
            selected_words_length += random_word.length;
            // If more than two words are selected
            if (selected_words.length > 2 && Math.random() > 0.6) {
                break;
            }
        }
        return selected_words;
    }

    function generateName() {
        let words = selectRandomWordsFromTitle();

        const name_formatting = Math.random();
        if (name_formatting < 0.5) {
            words = words.map(word => word[0].toUpperCase() + word.slice(1));
        } else if (name_formatting < 0.6) {
            words = words.map(word => word.toUpperCase());
        }

        const joining_chars = ['_', '-', ''];
        let joining_char = selectRandomly(joining_chars);
        let base_name = words.join(joining_char);

        if (Math.random() > 0.3 && base_name.length < 18) {
            const number_length = Math.floor(Math.random() * 5) + 1;
            const number = Math.floor(Math.random() * 10 ** number_length);
            base_name += number;
        }

        return base_name;
    }

    function timeAgo() {
      // Timestamp is str
        console.log(timestamp)
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        const diff_minutes = Math.floor(diff / 1000 / 60);
        const diff_hours = Math.floor(diff_minutes / 60);
        const diff_days = Math.floor(diff_hours / 24);
        const diff_weeks = Math.floor(diff_days / 7);
        const diff_months = Math.floor(diff_days / 30);
        const diff_years = Math.floor(diff_days / 365);

        if (diff_minutes < 1) {
            return 'just now';
        } else if (diff_hours < 1) {
            return `${diff_minutes} minutes ago`;
        } else if (diff_days < 1) {
            return `${diff_hours} hours ago`;
        } else if (diff_weeks < 1) {
            return `${diff_days} days ago`;
        } else if (diff_months < 1) {
            return `${diff_weeks} weeks ago`;
        } else if (diff_years < 1) {
            return `${diff_months} months ago`;
        } else {
            return `${diff_years} years ago`;
        }
    }

    function randomSentence() {
        const words = title.split(' ');

        // Generate a random sentence of length 40 to 80
        let sentence_length = Math.floor(Math.random() * 80) + 40;
        let sentence = '';
        while (sentence_length > 0) {
            let word = selectRandomly(words);
            sentence += word + ' ';
            sentence_length -= word.length;
        }
        return sentence;
    }

    const display_name = generateName();
    const display_timestamp = timeAgo();
    const display_sentence = randomSentence();

</script>

<div class="post" on:click={() => dispatch('selected', { url, verdict })}>
   <div class="post-header">
        <div class="post-description">
            Posted by u/{display_name}   {display_timestamp}
        </div>

        <span class="post-flair {class_verdict[verdict]}">
            {display_verdict[verdict]}
        </span> {title}
    </div>

    <div class="post-placeholder">
        {display_sentence}
    </div>
</div>
