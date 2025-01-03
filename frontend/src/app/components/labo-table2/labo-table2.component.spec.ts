import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LaboTable2Component } from './labo-table2.component';

describe('LaboTable2Component', () => {
  let component: LaboTable2Component;
  let fixture: ComponentFixture<LaboTable2Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LaboTable2Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LaboTable2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
