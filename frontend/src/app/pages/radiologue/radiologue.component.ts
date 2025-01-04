import { HeaderComponent } from '../../components/header/header.component';
import { RadioTableComponent } from '../../components/radio-table/radio-table.component'; 
import { Component } from '@angular/core';

@Component({
  selector: 'app-radiologue',
  imports: [HeaderComponent, RadioTableComponent], // Updated to radio-table
  templateUrl: './radiologue.component.html',
  styleUrls: ['./radiologue.component.scss']
})
export class RadiologueComponent {

}
