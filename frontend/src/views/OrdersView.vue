<template>
  <b-card
      title="Filters"
      tag="orders"
      class="mb-2"
  >
    <b-form inline>
      <div class="row">
        <div class="flex justify-content-center col-3">
          <label for="datepicker" class="justify-content-start">Delivery date</label>
          <b-form-input
              type="date"
              id="datepicker"
              class="col-3"
              v-model="deliveryDate"
              :date-format-options="{ year: 'numeric', month: 'short', day: '2-digit', weekday: 'short' }">
          </b-form-input>
        </div>
        <div class="col">
          <label>State</label>
          <div>
            <b-form-checkbox-group v-model="status">
              <b-form-checkbox value="in_progress">Process</b-form-checkbox>
              <b-form-checkbox value="submitted">Submitted</b-form-checkbox>
              <b-form-checkbox value="accepted">Accepted</b-form-checkbox>
              <b-form-checkbox value="invoiced">Invoiced</b-form-checkbox>
              <b-form-checkbox value="paid">Paid</b-form-checkbox>
              <b-form-checkbox value="cancelled">Cancelled</b-form-checkbox>
            </b-form-checkbox-group>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="ml-3 align-content-center col">
          <label for="customer" class="justify-content-start">Customer</label>
          <b-form-input id="customer" v-model="customer"></b-form-input>
        </div>
        <div class="ml-3  col">
          <label for="product" class="justify-content-start">Product</label>
          <b-form-input id="product" v-model="product"></b-form-input>
        </div>
      </div>
    </b-form>
  </b-card>

  <b-card>
    <template #header>
      <div class="row clear">
        <div class="col-4 align-content-center">
          <span class="fw-bold fs-4">Orders </span>
          <span class="inline fw-light fs-6" v-if="!data_loading">(Total {{ orders.length }})</span>
        </div>
        <div class="col text-right">
          <b-button variant="outline-primary"
                    size="sm"
                    :loading="init_loading"
                    @click.stop="initOrder2Server">
            S1: re-INIT Order
          </b-button>
          <b-button variant="outline-primary"
                    class="ms-2"
                    size="sm"
                    :loading="detail_syncing"
                    @click.stop="syncDetails">
            S2: Sync Detail
          </b-button>
        </div>
      </div>
    </template>
    <b-table-simple striped hover>
      <b-thead>
        <b-tr>
          <b-td v-for="h in fields">
            {{ h['label'] }}
          </b-td>
          <b-td>Action</b-td>
        </b-tr>
      </b-thead>
      <b-tbody>
        <template v-for="order in orders">
          <b-tr>
            <b-td v-for="h in fields">
              <template v-if="h.key === 'order_number'">
                <a :href="'https://app.fresho.com/supplier/orders/'+order.id" target="_blank">
                  {{ order[h['key']] }}
                </a>
              </template>
              <template v-else>
                {{ order[h['key']] }}
              </template>
            </b-td>
            <b-td>
              <b-button size="sm" @click="order.detailsShowing=!order.detailsShowing" class="mr-2"
                        variant="light">
                {{ order.detailsShowing ? 'Hide' : 'Show' }} Details
              </b-button>
            </b-td>
          </b-tr>
          <b-tr v-if="order.detailsShowing">
            <b-td :colspan="fields.length+1">
              <b-card>
                <div class="row" v-for="p in order.products">
                  <div class="col-2">{{ p.group }}</div>
                  <div class="col">{{ p.name }}</div>
                  <div class="col-2">{{ p.qty }} {{ p.qtyType }}</div>
                  <div class="col-1">{{ p.status }}</div>
                </div>
                <div v-if="!order.products">No Products</div>
              </b-card>
            </b-td>
          </b-tr>
        </template>

        <b-tr v-if="data_loading">
          <b-td :colspan="fields.length+1" class="text-center">
            <b-spinner label="Loading..."></b-spinner>
          </b-td>
        </b-tr>
        <b-tr v-if="!data_loading && orders.length===0">
          <b-td :colspan="fields.length+1" class="text-center">
            No Orders.
          </b-td>
        </b-tr>
      </b-tbody>
    </b-table-simple>
  </b-card>
</template>

<script lang="ts" setup>
import {ref, watch} from "vue";
import {CanceledError} from "axios";
import {getOrdersWithFilters, initOrders, syncOrderDetails, uploadOrdersCsv} from '@/api'

import {formatInTimeZone} from "date-fns-tz";

const localTZ = Intl.DateTimeFormat().resolvedOptions().timeZone

const deliveryDate = ref(formatInTimeZone(new Date(), localTZ, "yyyy-MM-dd"))
const customer = ref('')
const product = ref('')
const status = ref(['submitted', 'accepted', 'invoiced', 'paid'])

const orders = ref([])

const fields = [
  {key: 'order_number', label: 'Order#', sortable: true},
  {key: 'receiving_company_name', label: 'Customer', sortable: true},
  {key: 'state', label: 'State', sortable: true},
  {key: 'delivery_run', label: 'Run', sortable: true},
  {key: 'delivery_date', label: 'Date', sortable: true},
  // {key: 'show_details', label: 'Action'},
]

const init_loading = ref(false)
const detail_syncing = ref(false)
const data_loading = ref(false)

let abortController: AbortController | null = null;

const loading_data = async () => {

  data_loading.value = true
  orders.value = []
  if (abortController != null) {
    abortController.abort()
  }

  try {
    abortController = new AbortController()

    const data = (await getOrdersWithFilters({
          delivery_date: deliveryDate.value,
          customer: customer.value,
          product: product.value,
          status: status.value,
        },
        {signal: abortController.signal}
    )).data


    orders.value = data.map(function (x) {
      x.detailsShowing = false
      return x
    })

  } catch (e) {
    if (!(e instanceof CanceledError)) {
      console.error(e)
    }
  } finally {
    abortController = null
    data_loading.value = false
  }
}
const initOrder2Server = async () => {
  init_loading.value = true
  await initOrders(deliveryDate.value)
  init_loading.value = false
  await loading_data()
}
const syncDetails = async () => {
  detail_syncing.value = true
  await syncOrderDetails(deliveryDate.value)
  detail_syncing.value = false
  await loading_data()
}

watch([deliveryDate, customer, product, status], async ([]) => {
  await loading_data()
}, {immediate: true})

</script>
<style scoped>
tbody tr {
  cursor: pointer;
}

.text-right {
  text-align: right;
}
</style>