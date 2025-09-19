<script>
  import { getContext, onDestroy } from "svelte";
  import TextBlock from "../components/TextBlock.svelte";
  import { getTextByLang } from "../utils/getTextByLang";

  const languageStore = getContext("language");
  let lang;

  const unsubscribe = languageStore.subscribe((value) => {
    lang = value;
  });

  onDestroy(unsubscribe);
</script>

<section class="description">
  <TextBlock headerBlock={getTextByLang("headerBlockFirst", lang)}>
    <article class="description__text-wrapper">
      {@html getTextByLang("textBlockFirst", lang)}
    </article>
  </TextBlock>
</section>

<style>
  .description {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 980px;
    min-width: 375px;
    overflow-x: hidden;
  }

  .description__text-wrapper {
    align-items: center;
    padding-left: 30px;
    padding-right: 30px;
    line-height: 1.2em;
  }

  @media (max-width: 500px) {
    .description__text-wrapper {
      width: 375px;
    }
    .description {
      width: 375px;
    }
  }
</style>
