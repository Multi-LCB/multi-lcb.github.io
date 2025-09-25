<script lang="ts">
  import RangeSlider from "../components/RangeSlider.svelte";
  import { getContext, onDestroy, onMount } from "svelte";
  import { getTextByLang } from "../utils/getTextByLang";
  import { validationJson } from "../utils/validateJson";

  let currentSortKey: string | null = null;
  let sortDirection: "asc" | "desc" | null = null;
  let originalData: SummaryRow[] = [];

  const languageStore = getContext("language");
  let lang;
  const unsubscribe = languageStore.subscribe((value) => {
    lang = value;
  });

  const params = new URLSearchParams(window.location.search);
  let currentPage = params.get("page") || "home";
  console.log(currentPage);

  onDestroy(unsubscribe);

  // шаг в полтора месяц
  const step = 1000 * 60 * 60 * 24 * 40;

  interface DataRow {
    model: string;
    date: string;
    "pass@1[avg]": number;
    "pass@1[python]": number;
    "pass@1[javascript]": number;
    "pass@1[typescript]": number;
    "pass@1[java]": number;
    "pass@1[c++]": number;
    "pass@1[c#]": number;
    "pass@1[go]": number;
    "pass@1[rust]": number;
    "pass@1[ruby]": number;
    task_id: string;
  }

  interface SummaryRow {
    modelIdx: number;
    model: string;
    "pass@1[avg]": number;
    "pass@1[python]": number;
    "pass@1[javascript]": number;
    "pass@1[typescript]": number;
    "pass@1[java]": number;
    "pass@1[c++]": number;
    "pass@1[c#]": number;
    "pass@1[go]": number;
    "pass@1[rust]": number;
    "pass@1[ruby]": number;
    //pass1_std: number;
    //"pass@6": number;
    n_task: number;
    //trajectory?: string;
  }

  let calculatedByJsonData: SummaryRow[] = [];
  let filteredByDate: SummaryRow[] = [];
  let allData: DataRow[] = [];

  // подгрузка всех файлов
  const modelsDataModules = import.meta.glob("../data/*.json");
  let START_DATE: number;
  let END_DATE: number;

  // date range: [timestamp, timestamp]
  let dateRange;

  // Преобразуем JSON с колонками в массив DataRow
  function reshapeColumnJson(obj: any): DataRow[] {
    const keys = Object.keys(obj);
    const length = Object.values(obj[keys[0]]).length;
    return Array.from({ length }, (_, i) => {
      const row: Record<string, any> = {};
      keys.forEach((key) => {
        row[key] = obj[key][i];
      });
      return row as DataRow;
    });
  }

  // основные вычисления по файлам
  function summarize(data: DataRow[]): SummaryRow[] {
    const grouped = data.reduce(
      (acc, row) => {
        (acc[row.model] ||= []).push(row);
        return acc;
      },
      {} as Record<string, DataRow[]>
    );

    const mean = (arr: number[]) => arr.reduce((a, b) => a + b, 0) / arr.length;
    const std = (arr: number[]) => {
      const m = mean(arr);
      return Math.sqrt(arr.reduce((s, x) => s + (x - m) ** 2, 0) / arr.length);
    };

    // choose a display language key; adjust this mapping as needed
    // e.g., derive from `lang` if it represents a language slug
    const languageKey = "pass@1[avg]";

    const summary = Object.entries(grouped).map(([model, rows]) => {
      const pass1Lang = rows.map((r) => r[languageKey] ?? 0);
      const pass6 = rows.map((r: any) => r["pass@6"] ?? 0);
      const tasksLength = rows.length;

      
      return {
        modelIdx: 0,
        model,
        "pass@1[avg]": (mean(rows.map(r => r["pass@1[python]"] ?? 0)) * 100 + 
                        mean(rows.map(r => r["pass@1[javascript]"] ?? 0)) * 100 +
                        mean(rows.map(r => r["pass@1[typescript]"] ?? 0)) * 100 + 
                        mean(rows.map(r => r["pass@1[java]"] ?? 0)) * 100 + 
                        mean(rows.map(r => r["pass@1[c++]"] ?? 0)) * 100 + 
                        mean(rows.map(r => r["pass@1[c#]"] ?? 0)) * 100 + 
                        mean(rows.map(r => r["pass@1[go]"] ?? 0)) * 100 + 
                        mean(rows.map(r => r["pass@1[rust]"] ?? 0)) * 100 + 
                        mean(rows.map(r => r["pass@1[ruby]"] ?? 0)) * 100
                       ) / 9,
        "pass@1[python]": mean(rows.map(r => r["pass@1[python]"] ?? 0)) * 100,
        "pass@1[javascript]": mean(rows.map(r => r["pass@1[javascript]"] ?? 0)) * 100,
        "pass@1[typescript]": mean(rows.map(r => r["pass@1[typescript]"] ?? 0)) * 100,
        "pass@1[java]": mean(rows.map(r => r["pass@1[java]"] ?? 0)) * 100,
        "pass@1[c++]": mean(rows.map(r => r["pass@1[c++]"] ?? 0)) * 100,
        "pass@1[c#]": mean(rows.map(r => r["pass@1[c#]"] ?? 0)) * 100,
        "pass@1[go]": mean(rows.map(r => r["pass@1[go]"] ?? 0)) * 100,
        "pass@1[rust]": mean(rows.map(r => r["pass@1[rust]"] ?? 0)) * 100,
        "pass@1[ruby]": mean(rows.map(r => r["pass@1[ruby]"] ?? 0)) * 100,
        n_task: tasksLength,
      };
    });

    // Сортируем по выбранному языку pass@1[language] по убыванию
    summary.sort((a, b) => (b[languageKey as keyof SummaryRow] as number) - (a[languageKey as keyof SummaryRow] as number));
    summary.forEach((row, idx) => {
      row.modelIdx = idx + 1;
    });
    return summary;
  }

  function updateTable() {
    const filteredData = filterByDate(
      allData,
      new Date(dateRange[0]),
      new Date(dateRange[1])
    );
    calculatedByJsonData = summarize(filteredData);
    originalData = [...calculatedByJsonData];

    if (currentSortKey && sortDirection) {
      sortBy(currentSortKey, true);
    } else {
      filteredByDate = [...originalData];
    }
  }

  function filterByDate(data: DataRow[], start: Date, end: Date): DataRow[] {
    return data.filter((row) => {
      const date = new Date(row.date).getTime();
      return date >= start.getTime() && date <= end.getTime();
    });
  }

  function getMinimumDate(dataRow: DataRow[]) {
    let minimumDate = dataRow[0].date;
    for (let currentDate of dataRow) {
      if (new Date(minimumDate).getTime() > new Date(currentDate.date).getTime()) {
        minimumDate = currentDate.date;
      }
    }
    return new Date(minimumDate).getTime();
  }

  function getMaximumDate(dataRow: DataRow[]) {
    let maximumDate = dataRow[0].date;
    for (let currentDate of dataRow) {
      if (new Date(maximumDate).getTime() < new Date(currentDate.date).getTime()) {
        maximumDate = currentDate.date;
      }
    }
    return new Date(maximumDate).getTime();
  }

  function getClassByRank(idx: number) {
    switch (idx) {
      case 1:
        return "rank-badge rank-1";
      case 2:
        return "rank-badge rank-2";
      case 3:
        return "rank-badge rank-3";
      default:
        return "rank-badge rank-other";
    }
  }

  function sortBy(key: string, preserveDirection = false) {
    if (!preserveDirection) {
      if (currentSortKey === key) {
        if (sortDirection === "asc") {
          sortDirection = "desc";
        } else if (sortDirection === "desc") {
          sortDirection = null;
          currentSortKey = null;
          filteredByDate = [...originalData];
          return;
        } else {
          sortDirection = "asc";
        }
      } else {
        currentSortKey = key;
        sortDirection = "asc";
      }
    }
    filteredByDate = [...originalData].sort((a: any, b: any) => {
      const aVal = a[key];
      const bVal = b[key];
      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }

  // Загрузка и первичная агрегация
  onMount(async () => {
    try {
      const loadedData = await Promise.all(
        Object.values(modelsDataModules).map((module) => module())
      );
      loadedData.forEach((dataElement) => {
        validationJson(dataElement);
      });
      allData = loadedData.flatMap((result) => reshapeColumnJson(result.default));
      START_DATE = getMinimumDate(allData);
      END_DATE = getMaximumDate(allData);
      dateRange = [START_DATE, END_DATE];
    } catch (error) {
      console.error(error);
    }
  });

  // Реактивная реакция на изменение диапазона
  $: if (allData.length && dateRange) {
    updateTable();
  }
</script>

<section class="section-leaderboard">
  <div class="slider-wrapper">
    <RangeSlider
      id="testSlider"
      bind:values={dateRange}
      range
      float
      min={START_DATE}
      max={END_DATE}
      {step}
      all="label"
      pips
    />
  </div>

  {#if filteredByDate.length}
    <table style="width: 955px; overflow-x: auto; display: block;">
      <thead class="table__header">
<tr>
  <th class="table__header-position">{getTextByLang("position", lang)}</th>
  <th>{getTextByLang("model", lang)}</th>

  <!-- Sort by a specific language column; example shows python -->
  <th class="table__row-sort" on:click={() => sortBy("pass@1[avg]")}>
    <div class="cell-wrapper">
      pass@1[avg]
      {#if currentSortKey === "pass@1[avg]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[python]")}>
    <div class="cell-wrapper">
      pass@1[python]
      {#if currentSortKey === "pass@1[python]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[javascript]")}>
    <div class="cell-wrapper">
      pass@1[javascript]
      {#if currentSortKey === "pass@1[javascript]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[typescript]")}>
  <div class="cell-wrapper">
    pass@1[typescript]
    {#if currentSortKey === "pass@1[typescript]"}
      {#if sortDirection === "asc"}↑{/if}
      {#if sortDirection === "desc"}↓{/if}
    {:else}
      ↕
    {/if}
  </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[java]")}>
    <div class="cell-wrapper">
      pass@1[java]
      {#if currentSortKey === "pass@1[java]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[c++]")}>
    <div class="cell-wrapper">
      pass@1[c++]
      {#if currentSortKey === "pass@1[c++]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[c#]")}>
    <div class="cell-wrapper">
      pass@1[c#]
      {#if currentSortKey === "pass@1[c#]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[go]")}>
    <div class="cell-wrapper">
      pass@1[go]
      {#if currentSortKey === "pass@1[go]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[rust]")}>
    <div class="cell-wrapper">
      pass@1[rust]
      {#if currentSortKey === "pass@1[rust]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>
  <th class="table__row-sort" on:click={() => sortBy("pass@1[ruby]")}>
    <div class="cell-wrapper">
      pass@1[ruby]
      {#if currentSortKey === "pass@1[ruby]"}
        {#if sortDirection === "asc"}↑{/if}
        {#if sortDirection === "desc"}↓{/if}
      {:else}
        ↕
      {/if}
    </div>
  </th>     
  <th class="table__row-sort" on:click={() => sortBy("n_task")}>
  <div class="cell-wrapper">
    {getTextByLang("tasks", lang)}
    {#if currentSortKey === "n_task"}
      {#if sortDirection === "asc"}↑{/if}
      {#if sortDirection === "desc"}↓{/if}
    {:else}
      ↕
    {/if}
  </div>
  </th>
</tr>
</thead>

      <tbody>
        {#each filteredByDate as row}
          <tr class="table__row">
            <td class="table__position">
              <span class={getClassByRank(row.modelIdx)}>{row.modelIdx}</span>
            </td>
            <td class="table__row-cell">{row.model}</td>

            <!-- Display chosen language column; example shows python -->
            <td>{row["pass@1[avg]"].toFixed(2)}%</td>
            <td>{row["pass@1[python]"].toFixed(2)}%</td>
            <td>{row["pass@1[javascript]"].toFixed(2)}%</td>
            <td>{row["pass@1[typescript]"].toFixed(2)}%</td>
            <td>{row["pass@1[java]"].toFixed(2)}%</td>
            <td>{row["pass@1[c++]"].toFixed(2)}%</td>
            <td>{row["pass@1[c#]"].toFixed(2)}%</td>
            <td>{row["pass@1[go]"].toFixed(2)}%</td>
            <td>{row["pass@1[rust]"].toFixed(2)}%</td>
            <td>{row["pass@1[ruby]"].toFixed(2)}%</td>
            <td>{row.n_task}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <div class="table__no-data-wrapper">
      <span>{getTextByLang("notExistedData", lang)}</span>
    </div>
  {/if}
</section>

<style>
  .section-leaderboard {
    display: flex;
    flex-direction: column;
    padding-top: 20px;
    padding-right: 10px;
    padding-left: 10px;
    max-width: 1980px;
    width: 980px;
    min-height: 800px;
    border: 2px solid #d3d3d3;
    border-radius: 10px;
  }
  .slider-wrapper {
    margin: 20px;
  }
  table {
    display: table;
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    margin-bottom: 2rem;
    font-weight: 700;
    color: #1e293b;
  }
  .table__header {
    z-index: 2;
    position: sticky;
    top: 0;
  }
  .table__header-position {
    border-radius: 15px 0 0 15px;
  }
  .table__header-link {
    border-radius: 0 15px 15px 0;
    opacity: 1;
  }
  th,
  td {
    padding: 0.8rem 1.2rem;
    text-align: left;
  }
  tr {
    display: table-row;
    vertical-align: inherit;
    unicode-bidi: isolate;
  }
  th {
    background-color: #f4f4f4;
  }
  .table__row {
    border-bottom: 1px solid #ccc;
  }
  .table__row:hover {
    background-color: #f4f4f4;
  }
  .table__position {
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 800;
  }
  .cell-wrapper {
    display: flex;
    align-items: center;
  }
  .rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-weight: 700;
    font-size: 0.875rem;
    box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  }
  .rank-1 {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    color: #92400e;
  }
  .rank-2 {
    background: linear-gradient(135deg, #d1d5db, #9ca3af);
    color: #374151;
  }
  .rank-3 {
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: #9a3412;
  }
  .rank-other {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid var(--border);
  }
  .table__row-sort {
    white-space: nowrap;
    transition: all 0.5s ease;
    cursor: pointer;
  }
  .table__row-sort:hover {
    background: #e5e7eb;
  }
  .table__row-link {
    position: relative;
    color: #7d8da5;
  }
  .table__row-link::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: #7d8da5;
    transition: width 0.5s ease;
  }
  .table__row-link:hover::after {
    width: 100%;
  }
  @media (max-width: 500px) {
    .section-leaderboard {
      width: 375px;
      overflow: auto;
      padding-top: 0;
    }
    .slider-wrapper {
      width: 800px;
      margin-top: 40px;
    }
    td {
      padding: 0.2rem 0.4rem;
      text-align: left;
    }
  }
  .table__no-data-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 200px;
  }
</style>
