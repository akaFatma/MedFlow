// search-bar.component.ts
import { CommonModule } from '@angular/common';
import { Component, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter } from 'rxjs/operators';
import { OnInit } from '@angular/core';

@Component({
  selector: 'app-search-bar',
  imports: [CommonModule, FormsModule],
  templateUrl: './search-bar.component.html',
  styleUrl: './search-bar.component.scss'
})
export class SearchBarComponent implements OnInit {
  searchTerm: string = ''; // Changed to string to handle input properly
  private searchSubject = new Subject<string>();

  @Output() search: EventEmitter<number> = new EventEmitter<number>();
  @Output() scanQR: EventEmitter<void> = new EventEmitter<void>();

  ngOnInit() {
    // Set up debounced search
    this.searchSubject.pipe(
      debounceTime(300), // Wait 300ms after last input
      distinctUntilChanged(), // Only emit if value changed
      filter(term => {
        // Validate NSS format (assuming it should be numeric and have a minimum length)
        const numericTerm = parseInt(term, 10);
        return !isNaN(numericTerm) && term.length >= 5; // Adjust minimum length as needed
      })
    ).subscribe(term => {
      this.search.emit(parseInt(term, 10));
    });
  }

  onSearchChange(value: string): void {
    this.searchSubject.next(value);
  }

  onScanQR(): void {
    this.scanQR.emit();
  }
}