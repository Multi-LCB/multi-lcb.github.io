import Description from "./pages/Description.svelte";
import LeaderBoard from "./pages/LeaderBoard.svelte";
import NotFound from "./pages/NotFound.svelte";

 export default [
  {
    path: '/multi-lcb-page',
    component: Description
  },
  {
    path: "/multi-lcb-page/leaderboard",
    component: LeaderBoard
  },
  {
    path: "*",
    component: NotFound
  }
 ]