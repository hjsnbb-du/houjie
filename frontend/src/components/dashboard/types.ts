export interface WorkOrderStats {
  newToday: number;
  completedToday: number;
  totalCompleted: number;
  remaining: number;
}

export interface CustomerStats {
  total: number;
  active: number;
  followUp: number;
  expired: number;
}

export interface DashboardStats {
  workOrders: WorkOrderStats;
  customers: CustomerStats;
}

export interface TrendData {
  date: string;
  value: number;
  category?: string;
}

export interface DashboardTrends {
  workOrders: TrendData[];
  customers: TrendData[];
}
