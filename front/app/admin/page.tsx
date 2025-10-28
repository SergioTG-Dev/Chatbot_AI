import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { BarChartComponent } from '@/components/ui/barchart'; 

export default function AdminDashboardPage() {
  const totalChats = 5890;
  const completionRate = 82;
  const topIntents = [
    { name: 'Impuestos', value: 3500, fill: '#8884d8' },
    { name: 'Licencias', value: 1200, fill: '#82ca9d' },
    { name: 'Habilitaciones', value: 800, fill: '#ffc658' },
    { name: 'Partida de Nacimiento', value: 600, fill: '#d0ed57' },
    { name: 'Otros', value: 400, fill: '#a4de6c' },
  ];

  return (
    <>
        <h2 className="text-3xl font-semibold mb-6">Métricas de Rendimiento del Chatbot</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
          
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Conversaciones Totales</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-extrabold">{totalChats}</div>
              <p className="text-xs text-muted-foreground mt-1">+12% desde el mes pasado</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Tasa de Completitud</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-extrabold text-green-600">{completionRate}%</div>
              <p className="text-xs text-muted-foreground mt-1">Éxito en la resolución</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Tiempo Promedio de Respuesta</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-extrabold">0.8s</div>
              <p className="text-xs text-muted-foreground mt-1">Velocidad de la IA</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Fallas de Entendimiento</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-extrabold text-red-600">3%</div>
              <p className="text-xs text-muted-foreground mt-1">Requiere revisión de NLU</p>
            </CardContent>
          </Card>
        </div>


        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="col-span-1 lg:col-span-2">
            <CardHeader>
              <CardTitle>Top 3 Intenciones (Preguntas Frecuentes)</CardTitle>
            </CardHeader>
            <CardContent className="h-96">
                <BarChartComponent 
                    data={topIntents} 
                    dataKey="value" 
                    nameKey="name"
                    title="Número de Consultas"
                />
                <div className="text-muted-foreground text-center pt-20">
                    
                    <ul className="mt-4 list-disc list-inside text-left mx-auto w-fit">
                        {topIntents.map(intent => (
                            <li key={intent.name}>{intent.name}: {intent.value} consultas</li>
                        ))}
                    </ul>
                </div>
            </CardContent>
          </Card>
          
        </div>
    </>
  );
}