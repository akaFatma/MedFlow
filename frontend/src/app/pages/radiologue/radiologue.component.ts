import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { HeaderComponent } from '../../components/header/header.component';
import { LaboTable2Component } from '../../components/labo-table2/labo-table2.component'; // Updated to labo-table2
import { Component } from '@angular/core';

@Component({
  selector: 'app-radiologue',
  imports: [SidebarComponent, HeaderComponent, LaboTable2Component], // Updated to labo-table2
  templateUrl: './radiologue.component.html',
  styleUrls: ['./radiologue.component.scss']
})
export class RadiologueComponent {

}
