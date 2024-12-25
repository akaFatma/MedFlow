import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MedecinTableComponent } from './medecin-table.component';

describe('MedecinTableComponent', () => {
  let component: MedecinTableComponent;
  let fixture: ComponentFixture<MedecinTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MedecinTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MedecinTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
