import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PizzeriaService } from './services/pizzeria.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App implements OnInit {
  titulo = '';
  pedidos: any[] = [];
  vistaActual = 'lista';
  editandoId: number | null = null; 

  cliente = {
    nombre_cliente: '',
    direccion: '',
    telefono: '',
    fecha_pedido: new Date().toISOString().slice(0, 16) 
  };

  pizzaActual = {
    tamano: 'Chica', precioBase: 40,
    ingredientesSeleccionados: { jamon: false, pina: false, champinones: false },
    num_pizzas: 1
  };

  detallePedido: any[] = [];
  
  filtroDia = 'Lunes';
  filtroMes = 'Noviembre';
  resultadosReporte: any[] = [];
  totalReporte = 0;

  constructor(private pizzeriaService: PizzeriaService) {}

  ngOnInit() { this.cargarDatos(); }

  cargarDatos() {
    this.pizzeriaService.getPedidos().subscribe(data => this.pedidos = data);
  }

  cambiarVista(vista: string) {
    this.vistaActual = vista;
    if (vista === 'formulario') this.resetearFormulario();
  }

  resetearFormulario() {
    this.editandoId = null;
    this.cliente = { nombre_cliente: '', direccion: '', telefono: '', fecha_pedido: new Date().toISOString().slice(0, 16) };
    this.detallePedido = [];
    this.pizzaActual = { tamano: 'Chica', precioBase: 40, ingredientesSeleccionados: { jamon: false, pina: false, champinones: false }, num_pizzas: 1 };
  }

  actualizarPrecioBase() {
    if (this.pizzaActual.tamano === 'Chica') this.pizzaActual.precioBase = 40;
    else if (this.pizzaActual.tamano === 'Mediana') this.pizzaActual.precioBase = 80;
    else if (this.pizzaActual.tamano === 'Grande') this.pizzaActual.precioBase = 120;
  }

  agregarPizzaAlDetalle() {
    let costo = 0;
    let ingredientes = [];
    if (this.pizzaActual.ingredientesSeleccionados.jamon) { costo += 10; ingredientes.push('Jamón'); }
    if (this.pizzaActual.ingredientesSeleccionados.pina) { costo += 10; ingredientes.push('Piña'); }
    if (this.pizzaActual.ingredientesSeleccionados.champinones) { costo += 10; ingredientes.push('Champiñones'); }

    this.detallePedido.push({
      tamano: this.pizzaActual.tamano,
      ingredientes: ingredientes,
      num_pizzas: this.pizzaActual.num_pizzas,
      subtotal: (this.pizzaActual.precioBase + costo) * this.pizzaActual.num_pizzas
    });
    this.pizzaActual = { tamano: 'Chica', precioBase: 40, ingredientesSeleccionados: { jamon: false, pina: false, champinones: false }, num_pizzas: 1 };
  }

  quitarItemDetalle(index: number) { this.detallePedido.splice(index, 1); }

  calcularTotalGeneral(): number {
    return this.detallePedido.reduce((acc, item) => acc + item.subtotal, 0);
  }

  cargarParaEditar(pedido: any) {
    this.editandoId = pedido.id;
    this.cliente = {
      nombre_cliente: pedido.nombre_cliente,
      direccion: pedido.direccion,
      telefono: pedido.telefono,
      fecha_pedido: new Date(pedido.fecha_pedido).toISOString().slice(0, 16)
    };
    this.detallePedido = []; 
    this.cambiarVista('formulario');
    Swal.fire('Modo Edición', 'Edita los datos del cliente y vuelve a agregar las pizzas', 'info');
  }

  terminarPedido() {
    if (!this.cliente.nombre_cliente || !this.cliente.direccion) {
      Swal.fire('Atención', 'Complete los datos del cliente', 'warning');
      return;
    }
    if (this.detallePedido.length === 0) {
      Swal.fire('Atención', 'Debe agregar al menos una pizza', 'warning');
      return;
    }

    const pedidoFinal = { ...this.cliente, total_pedido: this.calcularTotalGeneral(), detalles: this.detallePedido };

    if (this.editandoId) {
      this.pizzeriaService.actualizarPedido(this.editandoId, pedidoFinal).subscribe(() => {
        Swal.fire('¡Actualizado!', 'El pedido fue modificado correctamente', 'success');
        this.cargarDatos();
        this.cambiarVista('lista');
      });
    } else {
      this.pizzeriaService.crearPedido(pedidoFinal).subscribe(() => {
        Swal.fire('¡Guardado!', `Total a pagar: $${pedidoFinal.total_pedido}`, 'success');
        this.cargarDatos();
        this.cambiarVista('lista');
      });
    }
  }

  eliminarPedido(id: number) {
    Swal.fire({
      title: '¿Estás seguro?',
      text: "No podrás revertir esto",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#e74c3c',
      cancelButtonColor: '#95a5a6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        this.pizzeriaService.eliminarPedido(id).subscribe(() => {
          Swal.fire('Eliminado', 'El pedido fue borrado.', 'success');
          this.cargarDatos();
        });
      }
    });
  }

  buscarVentasDia() {
    this.pizzeriaService.getVentasPorDia(this.filtroDia).subscribe(data => {
      this.resultadosReporte = data;
      this.totalReporte = data.reduce((acc: number, item: any) => acc + Number(item.total_pedido), 0);
    });
  }

  buscarVentasMes() {
    this.pizzeriaService.getVentasPorMes(this.filtroMes).subscribe(data => {
      this.resultadosReporte = data;
      this.totalReporte = data.reduce((acc: number, item: any) => acc + Number(item.total_pedido), 0);
    });
  }
}