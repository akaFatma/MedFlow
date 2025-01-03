import { Component } from '@angular/core';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { HeaderComponent } from '../../components/header/header.component';
import { LaboTableComponent } from '../../components/labo-table/labo-table.component';

@Component({
  selector: 'app-radiologue',
  imports: [SidebarComponent, HeaderComponent, LaboTableComponent],  // Add components here
  templateUrl: './radiologue.component.html',
  styleUrls: ['./radiologue.component.scss']  // Corrected from styleUrl to styleUrls
})
export class RadiologueComponent {
  // Your component logic here
}

