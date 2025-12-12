import type { Threat, ThreatsResponse, Provider, User } from '@/types'

export const mockThreats: Threat[] = [
  {
    id: '1',
    title: 'Malware détecté sur endpoint-001',
    description: 'Un malware de type Trojan a été détecté sur le système endpoint-001',
    severity: 'critical',
    status: 'active',
    provider: 'ninja',
    detectedAt: new Date(Date.now() - 3600000).toISOString(),
    metadata: { endpoint: 'endpoint-001', malwareType: 'Trojan' },
  },
  {
    id: '2',
    title: 'Tentative d\'intrusion réseau',
    description: 'Plusieurs tentatives de connexion suspectes détectées',
    severity: 'high',
    status: 'active',
    provider: 'malwarebytes',
    detectedAt: new Date(Date.now() - 7200000).toISOString(),
    metadata: { sourceIp: '192.168.1.100', attempts: 15 },
  },
  {
    id: '3',
    title: 'Vulnérabilité détectée',
    description: 'Vulnérabilité CVE-2024-1234 détectée sur plusieurs systèmes',
    severity: 'medium',
    status: 'pending',
    provider: 'ninja',
    detectedAt: new Date(Date.now() - 86400000).toISOString(),
    metadata: { cve: 'CVE-2024-1234', affectedSystems: 5 },
  },
  {
    id: '4',
    title: 'Phishing email détecté',
    description: 'Email de phishing identifié et bloqué',
    severity: 'low',
    status: 'resolved',
    provider: 'malwarebytes',
    detectedAt: new Date(Date.now() - 172800000).toISOString(),
    resolvedAt: new Date(Date.now() - 86400000).toISOString(),
    metadata: { email: 'suspicious@example.com' },
  },
  {
    id: '5',
    title: 'Ransomware détecté',
    description: 'Activité suspecte de ransomware détectée',
    severity: 'critical',
    status: 'active',
    provider: 'ninja',
    detectedAt: new Date(Date.now() - 1800000).toISOString(),
    metadata: { endpoint: 'endpoint-042', fileCount: 150 },
  },
]

export const mockThreatsResponse: ThreatsResponse = {
  ninja: {
    threats: mockThreats.filter((t) => t.provider === 'ninja'),
    status: 'success',
  },
  malwarebytes: {
    threats: mockThreats.filter((t) => t.provider === 'malwarebytes'),
    status: 'success',
  },
}

export const mockProviders: Provider[] = [
  {
    guid: 'provider-1',
    name: 'Ninja One Production',
    type: 'ninja',
    base_url: 'https://api.ninjaone.com',
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    guid: 'provider-2',
    name: 'Malwarebytes Enterprise',
    type: 'malwarebytes',
    base_url: 'https://api.malwarebytes.com',
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
]

export const mockUsers: User[] = [
  {
    guid: 'user-1',
    username: 'admin',
    email: 'admin@example.com',
    role: 'admin',
    is_active: true,
  },
  {
    guid: 'user-2',
    username: 'client1',
    email: 'client1@example.com',
    role: 'client',
    is_active: true,
  },
]

