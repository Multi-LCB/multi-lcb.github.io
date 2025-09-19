<script lang="ts">
  import type { Component } from "svelte";

  interface TextBlockProps {
    headerBlock: string;
  }

  const { headerBlock }: TextBlockProps = $props();
</script>

<div class="text-wrapper">
  <h2 class="text__header">{headerBlock}</h2>
  <slot />
</div>

<style>
  .text-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 30px;
    margin-bottom: 30px;
    max-width: 960px;
    font-size: clamp(0.875rem, 0.7153rem + 0.5941vw, 1.25rem);
  }

  .text__header {
    font-weight: 400;
    font-size: clamp(1.25rem, 0.7266rem + 1.9704vw, 2.5rem);
  }

  @media (max-width: 500px) {
    .text-wrapper {
      width: 410px;
    }
  }
</style>
