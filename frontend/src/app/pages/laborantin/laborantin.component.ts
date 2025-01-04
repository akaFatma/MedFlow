import { Component } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { LaboTableComponent } from '../../components/labo-table/labo-table.component';

@Component({
  selector: 'app-laborantin',
  standalone: true,
  imports: [HeaderComponent, LaboTableComponent],
  templateUrl: './laborantin.component.html',
  styleUrls: ['./laborantin.component.scss'],
})
export class LaborantinComponent {
  
}

