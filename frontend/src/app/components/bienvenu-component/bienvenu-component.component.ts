import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-bienvenu-component',
  templateUrl: './bienvenu-component.component.html',
  styleUrls: ['./bienvenu-component.component.scss'], // Corrected typo here
})
export class BienvenuComponentComponent {
  // Inputs to accept data from the parent component
 

  @Input() userName: string = '';
  @Input() firstName: string = '';
  // Corrected property name
  @Input() lastName: string = '';  // Corrected property name
}

// @Input() userName: string = '';