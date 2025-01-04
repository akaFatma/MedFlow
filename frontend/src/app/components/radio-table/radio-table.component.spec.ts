import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RadioTableComponent } from './radio-table.component';

describe('RadioTableComponent', () => {
  let component: RadioTableComponent;
  let fixture: ComponentFixture<RadioTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RadioTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RadioTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
