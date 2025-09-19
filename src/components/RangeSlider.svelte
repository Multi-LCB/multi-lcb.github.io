<script lang="ts">
  import { spring } from 'svelte/motion';
  import { createEventDispatcher } from 'svelte';
  import RangePips from './RangePips.svelte';

  export let range = false;
  export let pushy = false;
  export let min = 0;
  export let max = 100;
  export let step = 1;
  export let values = [(max + min) / 2];
  export let vertical = false;
  export let float = false;
  export let reversed = false;
  export let hoverable = true;
  export let disabled = false;
  export let uniqueDates = [];

  export let pips = false;
  export let pipstep = undefined;
  export let all = undefined;
  export let first = undefined;
  export let last = undefined;
  export let rest = undefined;

  export let id: string;
  export let prefix = '';
  export let suffix = '';
  export let formatter = (v, i, p) => v;
  export let handleFormatter = formatter;

  export let precision = 2;
  export let springValues = { stiffness: 0.15, damping: 0.4 };

  const dispatch = createEventDispatcher();

  let slider;

  let valueLength = 0;
  let focus = false;
  let handleActivated = false;
  let handlePressed = false;
  let keyboardActive = false;
  let activeHandle = values.length - 1;
  let startValue;
  let previousValue;

  let springPositions;

  $: {
    if (!Array.isArray(values)) {
      values = [(max + min) / 2];
      console.error(
        "'values' prop should be an Array (https://github.com/simeydotme/svelte-range-slider-pips#slider-props)",
      );
    }

    values = trimRange(values.map((v) => alignValueToStep(v)));
    if (valueLength !== values.length) {
      springPositions = spring(
        values.map((v) => percentOf(v)),
        springValues,
      );
    } else {
      springPositions.set(values.map((v) => percentOf(v)));
    }
    valueLength = values.length;
  }

  $: percentOf = function (val) {
    let perc = ((val - min) / (max - min)) * 100;
    if (isNaN(perc) || perc <= 0) {
      return 0;
    } else if (perc >= 100) {
      return 100;
    } else {
      return parseFloat(perc.toFixed(precision));
    }
  };

  $: clampValue = function (val) {
    return val <= min ? min : val >= max ? max : val;
  };

  $: alignValueToStep = function (val) {
    if (val <= min) {
      return min;
    } else if (val >= max) {
      return max;
    }

    let remainder = (val - min) % step;
    let aligned = val - remainder;
    if (Math.abs(remainder) * 2 >= step) {
      aligned += remainder > 0 ? step : -step;
    }
    aligned = clampValue(aligned);

    return parseFloat(aligned.toFixed(precision));
  };

  $: orientationStart = vertical
    ? reversed
      ? 'top'
      : 'bottom'
    : reversed
      ? 'right'
      : 'left';
  $: orientationEnd = vertical
    ? reversed
      ? 'bottom'
      : 'top'
    : reversed
      ? 'left'
      : 'right';

  function index(el) {
    if (!el) return -1;
    var i = 0;
    while ((el = el.previousElementSibling)) {
      i++;
    }
    return i;
  }

  function normalisedClient(e) {
    if (e.type.includes('touch')) {
      return e.touches[0];
    } else {
      return e;
    }
  }

  function targetIsHandle(el) {
    const handles = slider.querySelectorAll('.handle');
    const isHandle = Array.prototype.includes.call(handles, el);
    const isChild = Array.prototype.some.call(handles, (e) => e.contains(el));
    return isHandle || isChild;
  }

  function trimRange(values) {
    if (range === 'min' || range === 'max') {
      return values.slice(0, 1);
    } else if (range) {
      return values.slice(0, 2);
    } else {
      return values;
    }
  }

  function convertFromGetTimeToLocaleString(time: number): string {
    const timestamp = new Date(time);

    return changeDotsToSlashes(timestamp.toLocaleDateString());
  }

  function changeDotsToSlashes(convertedTime: string): string {
    return convertedTime.replaceAll('.', '/');
  }

  function getSliderDimensions() {
    return slider.getBoundingClientRect();
  }

  function getClosestHandle(clientPos) {
    const dims = getSliderDimensions();
    let handlePos = 0;
    let handlePercent = 0;
    let handleVal = 0;
    if (vertical) {
      handlePos = clientPos.clientY - dims.top;
      handlePercent = (handlePos / dims.height) * 100;
      handlePercent = reversed ? handlePercent : 100 - handlePercent;
    } else {
      handlePos = clientPos.clientX - dims.left;
      handlePercent = (handlePos / dims.width) * 100;
      handlePercent = reversed ? 100 - handlePercent : handlePercent;
    }
    handleVal = ((max - min) / 100) * handlePercent + min;

    let closest;

    if (range === true && values[0] === values[1]) {
      if (handleVal > values[1]) {
        return 1;
      } else {
        return 0;
      }
    } else {
      closest = values.indexOf(
        [...values].sort(
          (a, b) => Math.abs(handleVal - a) - Math.abs(handleVal - b),
        )[0],
      );
    }
    return closest;
  }

  function handleInteract(clientPos) {
    const dims = getSliderDimensions();
    let handlePos = 0;
    let handlePercent = 0;
    let handleVal = 0;
    if (vertical) {
      handlePos = clientPos.clientY - dims.top;
      handlePercent = (handlePos / dims.height) * 100;
      handlePercent = reversed ? handlePercent : 100 - handlePercent;
    } else {
      handlePos = clientPos.clientX - dims.left;
      handlePercent = (handlePos / dims.width) * 100;
      handlePercent = reversed ? 100 - handlePercent : handlePercent;
    }
    handleVal = ((max - min) / 100) * handlePercent + min;
    moveHandle(activeHandle, handleVal);
  }

  function moveHandle(index, value) {
    value = alignValueToStep(value);
    if (typeof index === 'undefined') {
      index = activeHandle;
    }
    if (range) {
      if (index === 0 && value > values[1]) {
        if (pushy) {
          values[1] = value;
        } else {
          value = values[1];
        }
      } else if (index === 1 && value < values[0]) {
        if (pushy) {
          values[0] = value;
        } else {
          value = values[0];
        }
      }
    }

    if (values[index] !== value) {
      values[index] = value;
    }

    if (previousValue !== value) {
      eChange();
      previousValue = value;
    }
    return value;
  }

  function rangeStart(values) {
    if (range === 'min') {
      return 0;
    } else {
      return values[0];
    }
  }

  function rangeEnd(values) {
    if (range === 'max') {
      return 0;
    } else if (range === 'min') {
      return 100 - values[0];
    } else {
      return 100 - values[1];
    }
  }

  function sliderBlurHandle(e) {
    if (keyboardActive) {
      focus = false;
      handleActivated = false;
      handlePressed = false;
    }
  }

  function sliderFocusHandle(e) {
    if (!disabled) {
      activeHandle = index(e.target);
      focus = true;
    }
  }

  function sliderKeydown(e) {
    if (!disabled) {
      const handle = index(e.target);
      let jump = e.ctrlKey || e.metaKey || e.shiftKey ? step * 10 : step;
      let prevent = false;

      switch (e.key) {
        case 'PageDown':
          jump *= 10;
        case 'ArrowRight':
        case 'ArrowUp':
          moveHandle(handle, values[handle] + jump);
          prevent = true;
          break;
        case 'PageUp':
          jump *= 10;
        case 'ArrowLeft':
        case 'ArrowDown':
          moveHandle(handle, values[handle] - jump);
          prevent = true;
          break;
        case 'Home':
          moveHandle(handle, min);
          prevent = true;
          break;
        case 'End':
          moveHandle(handle, max);
          prevent = true;
          break;
      }
      if (prevent) {
        e.preventDefault();
        e.stopPropagation();
      }
    }
  }

  function sliderInteractStart(e) {
    if (!disabled) {
      const el = e.target;
      const clientPos = normalisedClient(e);
      focus = true;
      handleActivated = true;
      handlePressed = true;
      activeHandle = getClosestHandle(clientPos);

      startValue = previousValue = alignValueToStep(values[activeHandle]);
      eStart();
      if (e.type === 'touchstart' && !el.matches('.pipVal')) {
        handleInteract(clientPos);
      }
    }
  }

  function sliderInteractEnd(e) {
    // fire the stop event for touch devices
    if (e.type === 'touchend') {
      eStop();
    }
    handlePressed = false;
  }

  function bodyInteractStart(e) {
    keyboardActive = false;
    if (focus && e.target !== slider && !slider.contains(e.target)) {
      focus = false;
    }
  }

  function bodyInteract(e) {
    if (!disabled) {
      if (handleActivated) {
        handleInteract(normalisedClient(e));
      }
    }
  }

  function bodyMouseUp(e) {
    if (!disabled) {
      const el = e.target;
      if (handleActivated) {
        if (el === slider || slider.contains(el)) {
          focus = true;
          if (!targetIsHandle(el) && !el.matches('.pipVal')) {
            handleInteract(normalisedClient(e));
          }
        }
        eStop();
      }
    }
    handleActivated = false;
    handlePressed = false;
  }

  function bodyTouchEnd(e) {
    handleActivated = false;
    handlePressed = false;
  }

  function bodyKeyDown(e) {
    if (!disabled) {
      if (e.target === slider || slider.contains(e.target)) {
        keyboardActive = true;
      }
    }
  }

  function eStart() {
    !disabled &&
      dispatch('start', {
        activeHandle,
        value: startValue,
        values: values.map((v) => alignValueToStep(v)),
      });
  }

  function eStop() {
    !disabled &&
      dispatch('stop', {
        activeHandle,
        startValue: startValue,
        value: values[activeHandle],
        values: values.map((v) => alignValueToStep(v)),
      });
  }

  function eChange() {
    !disabled &&
      dispatch('change', {
        activeHandle,
        startValue: startValue,
        previousValue:
          typeof previousValue === 'undefined' ? startValue : previousValue,
        value: values[activeHandle],
        values: values.map((v) => alignValueToStep(v)),
      });
  }
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  {id}
  bind:this={slider}
  class="rangeSlider"
  class:range
  class:disabled
  class:hoverable
  class:vertical
  class:reversed
  class:focus
  class:min={range === 'min'}
  class:max={range === 'max'}
  class:pips
  class:pip-labels={all === 'label' ||
    first === 'label' ||
    last === 'label' ||
    rest === 'label'}
  on:mousedown={sliderInteractStart}
  on:mouseup={sliderInteractEnd}
  on:touchstart|preventDefault={sliderInteractStart}
  on:touchend|preventDefault={sliderInteractEnd}
>
  {#each values as value, index}
    <span
      role="slider"
      class="rangeHandle"
      class:active={focus && activeHandle === index}
      class:press={handlePressed && activeHandle === index}
      data-handle={index}
      on:blur={sliderBlurHandle}
      on:focus={sliderFocusHandle}
      on:keydown={sliderKeydown}
      style="{orientationStart}: {$springPositions[
        index
      ]}%; z-index: {activeHandle === index ? 3 : 2};"
      aria-valuemin={range === true && index === 1 ? values[0] : min}
      aria-valuemax={range === true && index === 0 ? values[1] : max}
      aria-valuenow={value}
      aria-valuetext="{prefix}{handleFormatter(
        value,
        index,
        percentOf(value),
      )}{suffix}"
      aria-orientation={vertical ? 'vertical' : 'horizontal'}
      aria-disabled={disabled}
      tabindex={disabled ? -1 : 0}
    >
      <span class="rangeNub"></span>
      {#if float}
        <span class="rangeFloat">
          {#if prefix}<span class="rangeFloat-prefix"
              >{convertFromGetTimeToLocaleString(prefix)}</span
            >{/if}{convertFromGetTimeToLocaleString(value)}{#if suffix}<span
              class="rangeFloat-suffix">{suffix}</span
            >{/if}
        </span>
      {/if}
    </span>
  {/each}
  {#if range}
    <span
      class="rangeBar"
      style="{orientationStart}: {rangeStart($springPositions)}%; 
             {orientationEnd}: {rangeEnd($springPositions)}%;"
    ></span>
  {/if}
  {#if pips}
    <RangePips
      values={[0, 200]}
      {min}
      {max}
      {step}
      {range}
      {vertical}
      {reversed}
      {orientationStart}
      {orientationEnd}
      {hoverable}
      {disabled}
      {all}
      {first}
      {last}
      {rest}
      pipstep=3
      {prefix}
      {suffix}
      {formatter}
      {focus}
      {percentOf}
      {moveHandle}
      {uniqueDates}
    />
  {/if}
</div>

<svelte:window
  on:mousedown={bodyInteractStart}
  on:touchstart={bodyInteractStart}
  on:mousemove={bodyInteract}
  on:touchmove={bodyInteract}
  on:mouseup={bodyMouseUp}
  on:touchend={bodyTouchEnd}
  on:keydown={bodyKeyDown}
/>

<style>
  :global(.rangeSlider) {
    --slider: var(--range-slider, #d7dada);
    --handle-inactive: rgb(102, 126, 234);
    --handle: var(--range-handle, #838de7);
    --handle-focus: var(--range-handle-focus, #4a40d4);
    --handle-border: var(--range-handle-border, var(--handle));
    --range-inactive: var(--range-range-inactive, var(--handle-inactive));
    --range: var(--range-range, var(--handle-focus));
    --float-inactive: var(--range-float-inactive, var(--handle-inactive));
    --float: var(--range-float, var(--handle-focus));
    --float-text: var(--range-float-text, white);
  }
  :global(.rangeSlider) {
    position: relative;
    border-radius: 100px;
    height: 0.5em;
    margin: 1em;
    transition: opacity 0.2s ease;
    user-select: none;
  }
  :global(.rangeSlider *) {
    user-select: none;
  }
  :global(.rangeSlider.pips) {
    margin-bottom: 1.8em;
  }
  :global(.rangeSlider.pip-labels) {
    margin-bottom: 2.8em;
  }
  :global(.rangeSlider.vertical) {
    display: inline-block;
    border-radius: 100px;
    width: 0.5em;
    min-height: 200px;
  }
  :global(.rangeSlider.vertical.pips) {
    margin-right: 1.8em;
    margin-bottom: 1em;
  }
  :global(.rangeSlider.vertical.pip-labels) {
    margin-right: 2.8em;
    margin-bottom: 1em;
  }
  :global(.rangeSlider .rangeHandle) {
    position: absolute;
    display: block;
    height: 1.4em;
    width: 1.4em;
    top: 0.25em;
    bottom: auto;
    transform: translateY(-50%) translateX(-50%);
    z-index: 2;

    &:hover {
      cursor: pointer;
    }
  }
  :global(.rangeSlider.reversed .rangeHandle) {
    transform: translateY(-50%) translateX(50%);
  }
  :global(.rangeSlider.vertical .rangeHandle) {
    left: 0.25em;
    top: auto;
    transform: translateY(50%) translateX(-50%);
  }
  :global(.rangeSlider.vertical.reversed .rangeHandle) {
    transform: translateY(-50%) translateX(-50%);
  }
  :global(.rangeSlider .rangeNub),
  :global(.rangeSlider .rangeHandle:before) {
    position: absolute;
    left: 0;
    top: 0;
    display: block;
    border-radius: 10em;
    height: 100%;
    width: 100%;
    transition: box-shadow 0.2s ease;
  }
  :global(.rangeSlider .rangeHandle:before) {
    content: '';
    left: 1px;
    top: 1px;
    bottom: 1px;
    right: 1px;
    height: auto;
    width: auto;
    box-shadow: 0 0 0 0px var(--handle-border);
    opacity: 0;
  }
  :global(.rangeSlider.hoverable:not(.disabled) .rangeHandle:hover:before) {
    box-shadow: 0 0 0 8px var(--handle-border);
    opacity: 0.2;
  }
  :global(.rangeSlider.hoverable:not(.disabled) .rangeHandle.press:before),
  :global(
      .rangeSlider.hoverable:not(.disabled) .rangeHandle.press:hover:before
    ) {
    box-shadow: 0 0 0 12px var(--handle-border);
    opacity: 0.4;
  }
  :global(.rangeSlider.range:not(.min):not(.max) .rangeNub) {
    border-radius: 10em 10em 10em 1.6em;
  }
  :global(.rangeSlider.range .rangeHandle:nth-of-type(1) .rangeNub) {
    transform: rotate(-135deg);
  }
  :global(.rangeSlider.range .rangeHandle:nth-of-type(2) .rangeNub) {
    transform: rotate(45deg);
  }
  :global(.rangeSlider.range.reversed .rangeHandle:nth-of-type(1) .rangeNub) {
    transform: rotate(45deg);
  }
  :global(.rangeSlider.range.reversed .rangeHandle:nth-of-type(2) .rangeNub) {
    transform: rotate(-135deg);
  }
  :global(.rangeSlider.range.vertical .rangeHandle:nth-of-type(1) .rangeNub) {
    transform: rotate(135deg);
  }
  :global(.rangeSlider.range.vertical .rangeHandle:nth-of-type(2) .rangeNub) {
    transform: rotate(-45deg);
  }
  :global(
      .rangeSlider.range.vertical.reversed .rangeHandle:nth-of-type(1) .rangeNub
    ) {
    transform: rotate(-45deg);
  }
  :global(
      .rangeSlider.range.vertical.reversed .rangeHandle:nth-of-type(2) .rangeNub
    ) {
    transform: rotate(135deg);
  }
  :global(.rangeSlider .rangeFloat) {
    display: block;
    position: absolute;
    left: 50%;
    top: -0.5em;
    transform: translate(-50%, -100%);
    font-size: 1em;
    text-align: center;
    opacity: 1;
    pointer-events: none;
    white-space: nowrap;
    transition: all 0.2s ease;
    font-size: 0.9em;
    padding: 0.2em 0.4em;
    border-radius: 0.2em;
  }
  :global(.rangeSlider .rangeHandle.active .rangeFloat),
  :global(.rangeSlider .rangeHandle.hoverable:hover .rangeFloat) {
    opacity: 1;
    top: -0.2em;
    transform: translate(-50%, -100%);
  }
  :global(.rangeSlider .rangeBar) {
    position: absolute;
    display: block;
    transition: background 0.2s ease;
    border-radius: 1em;
    height: 0.5em;
    top: 0;
    user-select: none;
    z-index: 1;
  }
  :global(.rangeSlider.vertical .rangeBar) {
    width: 0.5em;
    height: auto;
  }
  :global(.rangeSlider) {
    background-color: #d7dada;
    background-color: var(--slider);
  }
  :global(.rangeSlider .rangeBar) {
    background-color: #99a2a2;
    background-color: var(--range-inactive);
  }
  :global(.rangeSlider.focus .rangeBar) {
    background-color: #838de7;
    background-color: var(--range);
  }
  :global(.rangeSlider .rangeNub) {
    background-color: rgb(102, 126, 234);
    background-color: var(--handle-inactive);
  }
  :global(.rangeSlider.focus .rangeNub) {
    background-color: #838de7;
    background-color: var(--handle);
  }
  :global(.rangeSlider .rangeHandle.active .rangeNub) {
    background-color: #4a40d4;
    background-color: var(--handle-focus);
  }
  :global(.rangeSlider .rangeFloat) {
    color: white;
    color: var(--float-text);
    background-color: #99a2a2;
    background-color: var(--float-inactive);
  }
  :global(.rangeSlider.focus .rangeFloat) {
    background-color: #4a40d4;
    background-color: var(--float);
  }
  :global(.rangeSlider.disabled) {
    opacity: 0.5;
  }
  :global(.rangeSlider.disabled .rangeNub) {
    background-color: #d7dada;
    background-color: var(--slider);
  }
</style>
