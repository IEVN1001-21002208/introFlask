import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PizzeriaService {
  private apiUrl = '/api';

  constructor(private http: HttpClient) {}

  getStatus(): Observable<any> {
    return this.http.get(`${this.apiUrl}/status`);
  }

  getPedidos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/pedidos`);
  }

  crearPedido(pedido: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/pedidos`, pedido);
  }

  actualizarPedido(id: number, pedido: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/pedidos/${id}`, pedido);
  }

  eliminarPedido(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/pedidos/${id}`);
  }

  getVentasPorDia(dia: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/ventas/dia/${dia}`);
  }

  getVentasPorMes(mes: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/ventas/mes/${mes}`);
  }
}