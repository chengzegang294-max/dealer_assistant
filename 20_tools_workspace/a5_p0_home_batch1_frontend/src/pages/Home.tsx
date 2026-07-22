import { EventStreamPanel } from "@/features/home/components/EventStreamPanel";
import { HomeHero } from "@/features/home/components/HomeHero";
import { HomeSidebar } from "@/features/home/components/HomeSidebar";
import { MainWorkspacePanel } from "@/features/home/components/MainWorkspacePanel";
import { StockSearchBar } from "@/features/home/components/StockSearchBar";
import { useHomePage } from "@/features/home/hooks/useHomePage";

export default function Home() {
  const {
    heroViewModel,
    eventStreamPanelProps,
    stockSearchBarProps,
    mainWorkspacePanelProps,
    homeSidebarProps,
  } = useHomePage();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col gap-6 px-4 py-6 lg:px-6">
        <header className="rounded-3xl border border-white/10 bg-slate-900/80 p-6 shadow-2xl shadow-slate-950/30">
          <div className="flex flex-col gap-5">
            <HomeHero {...heroViewModel} />
            <StockSearchBar
              {...stockSearchBarProps}
            />
          </div>
        </header>

        <main className="grid flex-1 gap-6 xl:grid-cols-[0.95fr_1.4fr_0.95fr]">
          <EventStreamPanel {...eventStreamPanelProps} />
          <MainWorkspacePanel {...mainWorkspacePanelProps} />
          <HomeSidebar {...homeSidebarProps} />
        </main>
      </div>
    </div>
  );
}
