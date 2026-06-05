import { useLocation, useNavigate } from 'react-router-dom'

const tabs = [
  { label: 'HOSPITAIS', icon: 'local_hospital', path: '/hospitais' },
  { label: 'RELATÓRIOS', icon: 'description', path: '/relatorio' },
]

export default function BottomNav() {
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <nav className="fixed bottom-0 w-full z-50 flex justify-around items-center px-container-margin py-3 bg-surface border-t border-outline-variant shadow-sm">
      {tabs.map((tab) => {
        const active = location.pathname === tab.path
        return (
          <button
            key={tab.path}
            onClick={() => navigate(tab.path)}
            className={`flex flex-col items-center justify-center transition-colors px-4 py-1 rounded-xl
              ${active
                ? 'bg-primary text-on-primary px-5 py-2'
                : 'text-on-surface-variant hover:text-primary'
              }`}
          >
            <span
              className="material-symbols-outlined"
              style={{ fontVariationSettings: active ? "'FILL' 1" : "'FILL' 0" }}
            >
              {tab.icon}
            </span>
            <span className="font-label-caps text-[10px] mt-1">{tab.label}</span>
          </button>
        )
      })}
    </nav>
  )
}
