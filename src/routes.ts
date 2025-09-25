import Description from "./pages/Description.svelte";
import LeaderBoard from "./pages/LeaderBoard.svelte";
import NotFound from "./pages/NotFound.svelte";

 export default [
  {
    path: '/live-lcb',
    component: Description
  },
  {
    path: "/live-lcb/leaderboard",
    component: LeaderBoard
  },
  {
    path: "*",
    component: NotFound
  }
 ]