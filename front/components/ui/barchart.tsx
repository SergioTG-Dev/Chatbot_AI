'use client';

import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  Cell
} from 'recharts';

interface BarChartComponentProps {
  data: Array<{ name: string; value: number; fill?: string }>;
  title?: string;
  dataKey: string;
  nameKey: string;
}

export const BarChartComponent = ({ data, title, dataKey, nameKey }: BarChartComponentProps) => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={nameKey} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar 
            dataKey={dataKey} 
            name={title || "Consultas"}
        >
            {data.map((entry, index) => (
                <Cell 
                    key={`cell-${index}`} 
                    fill={entry.fill || "#8884d8"}
                />
            ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};