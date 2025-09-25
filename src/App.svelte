<script>
  import router from "page";
  import NavigateButton from "./components/NavigateButton.svelte";
  import LeaderBoardIcon from "./assets/leaderBoarIcon.svg";
  import routes from "./routes";
  import ToggleSwitch from "./components/ToggleSwitch.svelte";
  import { getContext, onDestroy, setContext } from "svelte";
  import { language } from "./store/languageStore";
  import { getTextByLang } from "./utils/getTextByLang";
  import LinksHeaderButton from "./components/LinksHeaderButton.svelte";
  import logoLCB from "/logo.svg";
  import headerLogo from "/headerLogo.svg";
  import dataLogo from '/dataLogo.svg';
  import codeLogo from '/codeLogo.svg';
  import cupLogo from '/cupLogo.svg';
  let page;
  let params;

  setContext("language", language);

  const languageStore = getContext("language");
  let lang;

  const unsubscribe = languageStore.subscribe((value) => {
    lang = value;
  });

  onDestroy(unsubscribe);

  routes.forEach((route) => {
    router(
      route.path,
      (ctx, next) => {
        params = ctx.params;
        next();
      },

      () => {
        page = route.component;
      }
    );
  });


  router.start();
</script>

<header class="header">
  <a href="/live-lcb"
    ><img class="header-logo" src={headerLogo} alt="логотип" /></a
  >
  <div class="toggle-wrapper">
    <!-- Пока убрали эту кнопку, мб вернем) -->
    <!-- <NavigateButton
      buttonText={getTextByLang('home', lang)}
      imgSrc={HomeIcon}
      link="/"
    /> -->
    <NavigateButton
      buttonText={getTextByLang("leaderboard", lang)}
      imgSrc={LeaderBoardIcon}
      link="/live-lcb/leaderboard"
    />
    <ToggleSwitch
      bind:value={$language}
      design="multi"
      options={["eng", "ru"]}
      fontSize={14}
      label=""
    />
  </div>
</header>

<div class="intro-text">
  <img class="intro-logo" src={logoLCB} alt="Логотип" />
  <h3> <!-- class="intro__title"> -->
    {getTextByLang("header", lang)}
  </h3>
  <div class="intro-text__buttons-links">
    <LinksHeaderButton
      buttonText="Code"
      imgSrc={codeLogo}
      link="https://github.com/Multi-LCB/Multi-LiveCodeBench"
    />
    <LinksHeaderButton
      buttonText="Dataset TBD"
      imgSrc={dataLogo}
      link="https://huggingface.co/datasets/"
    />
    <LinksHeaderButton
      buttonText="Submit TBD"
      imgSrc={cupLogo}
      link="https://github.com/Multi-LCB/Multi-LiveCodeBench"
    />
  </div>
</div>
<main class="main-wrapper">
  <svelte:component this={page} {params} />
</main>

<style>
  .main-wrapper {
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-top: 50px;
    margin-bottom: 50px;
  }

  .header {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0 auto;
    width: 100%;
    height: 80px;
    background: linear-gradient(
      135deg,
      rgb(255, 231, 170) 0%,
      rgb(118, 75, 162) 100%
    );
    border-radius: 0 0 20px 20px;
  }

  .header-logo {
    margin-left: 16px;
    transition: 0.5s transform ease;
    &:hover {
      transform: scale(1.1);
      cursor: pointer;
    }
  }

  .intro-text {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    margin-top: 100px;
    max-width: 960px;
    text-align: center;
  }

  .intro-text__buttons-links {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }

  .intro-logo {
    width: 596px;
    height: 156px;
  }

  .intro__title {
    width: 780px;
    height: 40px;
    margin-bottom: 100px;
    font-size: clamp(1.75rem, 1.2266rem + 1.9704vw, 3rem);
    font-weight: 800;
  }

  .toggle-wrapper {
    display: flex;
    justify-content: end;
    width: 80%;
    gap: 30px;
    align-items: center;
    margin-right: 24px;
  }

  @media (max-width: 500px) {
    .header {
      justify-content: center;
      width: 100%;
    }

    .header-logo {
      width: 100px;
    }

    .intro__title {
      margin-bottom: 20px;
      padding-left: 10px;
      padding-right: 10px;
      width: 375px;
      height: 75px;
    }

    .intro-logo {
      width: 248px;
      height: 78px;
    }

    .toggle-wrapper {
      width: 100%;
    }

    .main-wrapper {
      margin-top: 10px;
      margin-bottom: 20px;
    }
  }
</style>
