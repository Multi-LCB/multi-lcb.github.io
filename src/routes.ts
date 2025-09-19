import Description from "./pages/Description.svelte";
import LeaderBoard from "./pages/LeaderBoard.svelte";
import NotFound from "./pages/NotFound.svelte";

 export default [
  {
    path: '/demo-swe-mera',
    component: Description
  },
  {
    path: "/demo-swe-mera/leaderboard",
    component: LeaderBoard
  },
  {
    path: "*",
    component: NotFound
  }
 ]