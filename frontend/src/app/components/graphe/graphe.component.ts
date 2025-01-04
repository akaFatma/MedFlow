import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Chart, ChartConfiguration, ChartOptions } from 'chart.js';

@Component({
  selector: 'app-graphe',
  templateUrl: './graphe.component.html',
  styleUrls: ['./graphe.component.scss']
})
export class GrapheComponent implements OnInit {
  bilanId: string | null = null;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    // Retrieve 'bilanId' from query params
    this.route.queryParams.subscribe(params => {
      this.bilanId = params['bilanId'];
      console.log('Bilan ID in GrapheComponent:', this.bilanId);

      // Generate the graph after getting bilanId
      this.generateGraph();
    });
  }

  generateGraph(): void {
    const barChartOptions: ChartOptions<'bar'> = {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        tooltip: { enabled: true },
      },
      scales: {
        x: {
          title: { display: true, text: 'Catégories' },
        },
        y: {
          title: { display: true, text: 'Valeurs' },
        },
      },
    };

    const barChartData: ChartConfiguration<'bar'>['data'] = {
      labels: ['Cholestérol', 'Hémoglobine A1c', 'Fer', 'Hypertension'],
      datasets: [
        {
          label: 'Précédent',
          data: [10, 15, 5, 100], // Placeholder data
          backgroundColor: 'red',
          borderWidth: 1,
        },
        {
          label: 'Actuel',
          data: [20, 18, 10, 200], // Placeholder data
          backgroundColor: 'blue',
          borderWidth: 1,
        },
      ],
    };

    const ctx = document.getElementById('barChart') as HTMLCanvasElement;

    if (ctx) {
      new Chart(ctx, {
        type: 'bar',
        data: barChartData,
        options: barChartOptions,
      });
    }
  }
}


// public barChartOptions: ChartOptions<'bar'> = {
//     responsive: true,
//     plugins: {
//       legend: {
//         position: 'top',
//       },
//       tooltip: {
//         enabled: true,
//       },
//     },
//     scales: {
//       x: {
//         title: {
//           display: true,
//           text: 'Catégories',
//         },
//       },
//       y: {
//         title: {
//           display: true,
//           text: 'Valeurs',
//         },
//       },
//     },
//   };

// public barChartData: ChartConfiguration<'bar'>['data'] = {
//     labels: ['Cholestérol', 'Hémoglobine A1c', 'Fer', 'Hypertension'],
//     datasets: [
//       {
//         label: 'Précédent',
//         data: [0, 0, 0, 0], // Placeholder data
//         backgroundColor: 'red',
//         borderWidth: 1,
//       },
//       {
//         label: 'Actuel',
//         data: [0, 0, 0, 0], // Placeholder data
//         backgroundColor: 'blue',
//         borderWidth: 1,
//       },
//     ],
//   };

// constructor(private route: ActivatedRoute) {}

// ngOnInit(): void {
//     // Retrieve 'bilanId' from query parameters
//     this.route.queryParams.subscribe(params => {
//         this.bilanId = params['bilanId']; // Use 'bilanId' instead of 'id'
//         console.log('Bilan ID in GrapheComponent:', this.bilanId);

//         // Fetch data for the graph based on 'bilanId' (implement fetch logic here)
//         this.updateGraphData(this.bilanId);
//     });
// }

// private updateGraphData(bilanId: string | null): void {
//     // Placeholder logic to simulate fetching data
//     if (bilanId === '1') {
//         this.barChartData.datasets[0].data = [10, 15, 5, 100]; // Précédent
//         this.barChartData.datasets[1].data = [20, 18, 10, 200]; // Actuel
//     } else if (bilanId === '2') {
//         this.barChartData.datasets[0].data = [5, 8, 12, 150];
//         this.barChartData.datasets[1].data = [7, 10, 15, 180];
//     } else {
//         this.barChartData.datasets[0].data = [0, 0, 0, 0]; // Default empty data
//         this.barChartData.datasets[1].data = [0, 0, 0, 0];
//     }

//     // Log to verify the updated data
//     console.log('Updated Chart Data:', this.barChartData);
// }
