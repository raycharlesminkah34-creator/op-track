import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import OpportunitiesList from './pages/OpportunitiesList'
import OpportunityDetail from './pages/OpportunityDetail'
import OpportunityForm from './pages/OpportunityForm'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="opportunities" element={<OpportunitiesList />} />
          <Route path="opportunities/new" element={<OpportunityForm />} />
          <Route path="opportunities/:id" element={<OpportunityDetail />} />
          <Route path="opportunities/:id/edit" element={<OpportunityForm />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
