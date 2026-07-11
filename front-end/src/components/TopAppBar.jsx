export default function TopAppBar() {
  return (
    <header className="bg-surface fixed top-0 w-full z-50 flex justify-between items-center px-container-margin h-14 border-b border-outline-variant">
      <div className="flex items-center gap-xs">
        <span className="material-symbols-outlined text-primary">medical_services</span>
        <h1 className="font-headline-sm text-headline-sm text-primary">Soromais</h1>
      </div>
    </header>
  )
}
