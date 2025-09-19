<script lang="ts">
  interface NavigateButtonProps {
    imgSrc: string;
    link: string;
    buttonText: string;
  }

  let props: NavigateButtonProps = $props();
</script>

<a class="link-wrapper" href={props.link}>
  <img class="link-wrapper-link" src={props.imgSrc} alt="Иконка" />
  {props.buttonText}
</a>

<style>
  .link-wrapper {
    font-size: clamp(0.6875rem, 0.5074rem + 0.6863vw, 1.125rem);
    display: flex;
    justify-content: space-around;
    padding: 5px 10px;
    border-radius: 10px;
    border: 1px solid #fff;
    background: linear-gradient(
      135deg,
      rgb(118, 75, 162) 0%,
      rgb(255, 231, 170) 100%
      
    );
    color: #fff;
    transition: transform 0.5s;
  }

  .link-wrapper:hover {
    transform: scale(1.05);
  }

  .link-wrapper-link {
    max-width: 16px;
  }

  @media (max-width: 500px) {
    .link-wrapper {
      width: 75px;
    }
  }
</style>
