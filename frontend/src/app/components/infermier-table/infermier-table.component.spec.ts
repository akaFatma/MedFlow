import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfermierTableComponent } from './infermier-table.component';

describe('InfermierTableComponent', () => {
  let component: InfermierTableComponent;
  let fixture: ComponentFixture<InfermierTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InfermierTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InfermierTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
