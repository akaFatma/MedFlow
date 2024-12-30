import { Component } from '@angular/core';
import { Input } from '@angular/core';

@Component({
  selector: 'app-bienvenu-component',
  imports: [],
  templateUrl: './bienvenu-component.component.html',
  styleUrl: './bienvenu-component.component.scss'
})
export class BienvenuComponentComponent {
 
  @Input() first_name: string = '';
  @Input() last_name: string = '';

}
