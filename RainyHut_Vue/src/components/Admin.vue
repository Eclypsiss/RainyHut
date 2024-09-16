<template>
  <div class="common-layout">
    <el-container class="main-container">
      <el-header class="header">
        Manage
        <el-button color="white" :icon="SetUp" circle class="custom-button2" @click="goToAdmin" />
        <el-button color="white" class="custom-button3" round @click="goToMenu">Menu</el-button>
      </el-header>

      <el-container>
        <el-aside class="aside" width="200px">
          <h5 class="mb-2">分类</h5>
          <el-menu default-active="1" class="el-menu-vertical-demo">
            <el-menu-item index="1" @click="selectType('order')" class="menu-item">订单</el-menu-item>
            <el-menu-item index="2" @click="selectType('table')" class="menu-item">餐桌</el-menu-item>
            <el-menu-item index="3" @click="selectType('material')" class="menu-item">食材</el-menu-item>
            <el-menu-item index="4" @click="selectType('expense')" class="menu-item">费用</el-menu-item>
          </el-menu>
        </el-aside>

        <el-main>
          <div class="order_container" v-if="currentType === 'order'">
            <div class="order_list">
              <div v-for="order in filteredOrders" :key="order.OrderID" class="order_item">
                <div class="order_info">
                  <h3>订单编号: {{ order.OrderID }}</h3>
                  <p>订单类型: {{ order.OrderType === 'takeaway' ? '外卖' : '堂食' }}</p>

                  <!-- 根据订单类型条件渲染桌号或配送地址 -->
                  <p>
                    {{ order.OrderType === 'takeaway'
                      ? `配送地址: ${order.Takeaway ? order.Takeaway.TakeawayAdd : '无'}`
                      : `桌号: ${order.Table ? order.Table : '无'}` }}
                  </p>

                  <p>总金额: ${{ order.TotalAmount }}</p>
                  <p>订单状态: {{ order.OrderStatus === 'finished' ? '已完成' : '进行中' }}</p>
                  <el-button color="white" :icon="List" class="custom-button1" circle @click="openOrderDialog(order)" />
                </div>
              </div>
            </div>
            <el-dialog v-model="dialogVisible"  class="custom-dialog">
              <div class="dialog-content">
                <h3>订单详情</h3>
                <p>订单编号: {{ selectedOrder.OrderID }}</p>
                <p>总金额: ${{ selectedOrder.TotalAmount }}</p>
                <p>订单状态: {{ selectedOrder.OrderStatus }}</p>
                <hr class="separator" />
                <ul class="dish-list">
                  <li v-for="(dish, index) in selectedOrder.Dishes" :key="index">
                    {{ dish.DishName }} - 数量: {{ dish.Quantity }} - 价格: ${{ dish.DishPrice }}
                  </li>
                </ul>
              </div>
              <span slot="footer" class="dialog-footer">
                <el-button color="white" class="custom-button6" round @click="closeDialog">取消</el-button>
                <el-button
                  v-if="selectedOrder.OrderStatus === 'in_progress'"
                  color="#76c02f" class="custom-button6" round
                  @click="completeOrder">完成
                </el-button>
              </span>
            </el-dialog>
          </div>

          <div class="table_container" v-if="currentType === 'table'">
            <div class="table_list">
              <div v-for="table in filteredTables" :key="table.TableID" class="table_item">
                <div class="table_info">
                  <h3>餐桌编号: {{ table.TableID }}</h3>
                  <p>状态: {{ table.TableStatus === 'in_use' ? '使用中' : table.TableStatus === 'available' ? '空闲' : table.TableStatus }}</p>
                  <el-button v-if="table.TableStatus === 'in_use'" color="white" :icon="List" class="custom-button5" circle @click="openTableDialog(table.TableID)" />
                </div>
              </div>
              <el-dialog v-model="tableDialogVisible" class="custom-dialog">
                <div class="dialog-content">
                  <div v-if="Object.keys(currentTableOrder).length > 0">
                    <h3>当前餐桌订单详情</h3>
                    <p>订单编号: {{ currentTableOrder.OrderID }}</p>
                    <p>总金额: ${{ currentTableOrder.TotalAmount }}</p>
                    <hr class="separator" />
                    <ul class="dish-list">
                      <li v-for="(dish, index) in currentTableOrder.Dishes" :key="index">
                        {{ dish.DishName }} - 数量: {{ dish.Quantity }} - 价格: ${{ dish.DishPrice }}
                      </li>
                    </ul>
                  </div>
                  <div v-else>
                    <p>当前餐桌没有相关订单。</p>
                  </div>
                </div>
                <span slot="footer" class="dialog-footer">
                  <el-button color="white" round class="custom-button6" @click="closeTableDialog">关闭</el-button>
                </span>
              </el-dialog>
            </div>
          </div>

          <div class="material_container" v-if="currentType === 'material'">
            <div class="material_list">
              <div v-for="material in filteredMaterials" :key="material.MaterialID" class="material_item">
                <div class="material_info">
                  <h3>食材名称: {{ material.MaterialName === 'Vegetable' ? '蔬果' : material.MaterialName === 'Meat' ? '肉类' : material.MaterialName === 'Seafood' ? '海鲜' : material.MaterialName }}</h3>
                  <p>数量: {{ material.Stock }}</p>
                  <p>单价: ${{ material.MaterialPrice }}</p>
                  <el-button color="white" :icon="Plus" circle class="custom-button4" @click="buyMaterial(material)"/>
                </div>
                <el-dialog v-model="buyDialogVisible" title="购买食材">
                  <el-form label-width="100px">
                    <el-form-item label="数量">
                      <el-input v-model.number="buyQuantity" type="number" placeholder="请输入数量" />
                    </el-form-item>
                    <el-form-item label="总金额">
                      <p>${{ totalCost }}</p>
                    </el-form-item>
                  </el-form>
                  <span slot="footer" class="dialog-footer">
                    <el-button color="white" round class="custom-button6" @click="closeBuyDialog">取消</el-button>
                    <el-button color="#76c02f" round class="custom-button6" @click="confirmPurchase">购买</el-button>
                  </span>
                </el-dialog>
              </div>
            </div>
          </div>

          <div class="expense_container" v-if="currentType === 'expense'">
            <el-button color="white" @click="calculateTotal" round class="total_button">计算总费用</el-button>
            <el-button color="white" @click="openExpenseDialog" round class="add_expense">添加费用</el-button>

            <div class="expense_list">
              <div v-for="expense in filteredExpenses" :key="expense.ExpenseID" class="expense_item">
                <div class="expense_info">
                  <h3>
                    费用类型:
                    <span v-if="expense.ExpenseType === 'order'">订单</span>
                    <span v-else-if="expense.ExpenseType === 'other'">其他</span>
                    <span v-else>{{ expense.ExpenseType }}</span>
                  </h3>
                  <p>订单编号: {{ expense.Order }}</p>
                  <p>费用金额: ${{ expense.ExpenseAmount }}</p>
                  <p>记录日期: {{ expense.Date }}</p>
                </div>
              </div>
            </div>

            <el-dialog title="总收入统计" v-model="totalDialogVisible" width="30%">
              <p>总收入: ${{ totalIncome }}</p>
              <span slot="footer" class="dialog-footer">
                <el-button color="white" round class="custom-button6" @click="totalDialogVisible = false">关闭</el-button>
              </span>
            </el-dialog>

            <el-dialog title="添加费用" v-model="dialogVisible2">
              <el-form label-width="100px">
                <el-form-item label="费用金额">
                  <el-input v-model.number="expenseAmount" type="number" placeholder="请输入费用金额" />
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button color="white" round class="custom-button6" @click="closeExpenseDialog">取消</el-button>
                <el-button color="#76c02f" round class="custom-button6" @click="saveExpense">确定</el-button>
              </span>
            </el-dialog>
          </div>

        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import {Delete, List, Plus, SetUp} from "@element-plus/icons-vue";
import axios from "axios";
const dialogTableVisible = ref(false)
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
export default {
  name: 'AdminPage',
  computed: {
    totalCost() {
      if (this.selectedMaterial) {
        return this.selectedMaterial.MaterialPrice * this.buyQuantity;
      }
      return 0;
    },

    List() {
      return List
    },
    Plus() {
      return Plus
    },
    SetUp() {
      return SetUp
    },
    Delete() {
      return Delete
    }
  },
  data() {
    return {
      currentType: 'order',

      filteredOrders: [],
      dialogVisible: false,
      selectedOrder: {},

      filteredTables: [],
      filteredMaterials: [],
      filteredExpenses: [],

      totalIncome: 0,
      totalDialogVisible: false,

      dialogVisible2: false,
      expenseAmount: 0,

      tableDialogVisible: false,
      currentTableOrder: {},

      buyDialogVisible: false,
      buyQuantity: 1,
      selectedMaterial: null,
    };
  },

  created() {
    this.getOrders();
    this.getExpenses();
  },
  methods: {
    async getOrders() {
      try {
        const response = await this.$http.get('http://localhost:8000/api/order');
        this.filteredOrders = response.data;

        for (const order of this.filteredOrders) {
          const orderResponse = await this.$http.get(`http://localhost:8000/api/orders/${order.OrderID}/`); // 获取详细订单信息
          order.Dishes = orderResponse.data.Dishes;
        }

        console.log(this.filteredOrders);
      } catch (error) {
        console.error("获取订单数据失败:", error);
      }
    },
    openOrderDialog(order) {
      this.selectedOrder = order;
      this.dialogVisible = true;
    },
    closeDialog() {
      this.dialogVisible = false;
    },
    async completeOrder() {
      const baseUrl = 'http://localhost:8000';

      try {
        const response = await axios.put(`${baseUrl}/api/orders/${this.selectedOrder.OrderID}/`, {
          OrderStatus: 'finished',
        });

        const data = response.data;
        const tableID = this.selectedOrder.Table;

        if (this.selectedOrder.order_type !== 'takeaway' && tableID) {
          const tableResponse = await axios.get(`${baseUrl}/api/tables/${tableID}/status/`);
          const tableData = tableResponse.data;
          const tableStatus = tableData.status;

          if (tableStatus === 'in_use') {
            await axios.put(`${baseUrl}/api/tables/${tableID}/status/`, {
              TableStatus: 'available'
            });
          }
        }

        const totalAmount = this.selectedOrder.TotalAmount;
        await this.recordIncome(totalAmount);

        this.closeDialog();
        this.$message.success('订单已完成！');
      } catch (error) {
        console.error('完成订单时出错:', error);
        this.$message.error('完成订单时出错，请稍后再试。');
      }
    },

    async recordIncome(amount) {
        const incomeData = {
            ExpenseType: 'order',
            ExpenseAmount: amount,
            Date: new Date().toISOString().split('T')[0],
            Order: this.selectedOrder.OrderID
        };

        console.log('要发送的费用记录数据:', incomeData);

        try {
            const response = await fetch('http://localhost:8000/api/expenses/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(incomeData),
            });

            if (!response.ok) {
                const errorMessage = await response.json();
                throw new Error(errorMessage.error || '费用记录创建失败');
            }

            console.log('费用记录已成功创建');
        } catch (error) {
            console.error('记录收入时出错:', error.message);
        }
    },

    closeBuyDialog() {
      this.buyDialogVisible = false;
    },
    async confirmPurchase() {
        await this.updateMaterialAndRecordExpense();
    },

    async updateMaterialAndRecordExpense() {
        const quantity = this.buyQuantity;
        const materialId = this.selectedMaterial.MaterialID;
        const totalCost = this.selectedMaterial.MaterialPrice * quantity;

        try {
            const updateResponse = await axios.put(`http://localhost:8000/api/materials/${materialId}/update/`, {
                quantity: quantity,
            });

            const expenseData = {
                ExpenseType: 'other',
                ExpenseAmount: -totalCost,
                Date: new Date().toISOString().split('T')[0],
                Order: null
            };

            const expenseResponse = await fetch('http://localhost:8000/api/expenses/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(expenseData),
            });

            if (!expenseResponse.ok) {
                const errorMessage = await expenseResponse.json();
                throw new Error(errorMessage.error || '记录支出失败');
            }

            console.log('支出记录已成功创建');
            await this.getMaterials();
            this.closeBuyDialog();
            this.$message.success('购买成功！');
        } catch (error) {
            console.error('更新材料或记录支出时出错:', error.message);
        }
    },

    buyMaterial(material) {
      this.selectedMaterial = material;
      this.buyDialogVisible = true;
    },

    async getTables() {
      try {
        const response = await this.$http.get('http://localhost:8000/api/tables');
        this.filteredTables = response.data;
        console.log(this.filteredTables);
      } catch (error) {
        console.error("获取餐桌数据失败:", error);
      }
    },
    async getMaterials() {
      try {
        const response = await this.$http.get('http://localhost:8000/api/materials');
        this.filteredMaterials = response.data;
        console.log(this.filteredMaterials);
      } catch (error) {
        console.error("获取食材数据失败:", error);
      }
    },
    async getExpenses() {
      try {
        const response = await this.$http.get('http://localhost:8000/api/expenses');
        this.filteredExpenses = response.data;

        if (Array.isArray(this.filteredExpenses)) {
          console.log("获取到的费用数据:", this.filteredExpenses);
        } else {
          console.error("获取数据不是数组:", this.filteredExpenses);
          this.filteredExpenses = [];
        }
      } catch (error) {
        console.error("获取费用数据失败:", error);
      }
    },

    calculateTotal() {
      if (!Array.isArray(this.filteredExpenses)) {
        console.error('filteredExpenses 不是数组:', this.filteredExpenses);
        return;
      }

      const total = this.filteredExpenses.reduce((acc, expense) => {
        const amount = parseFloat(expense.ExpenseAmount);
        return acc + (isNaN(amount) ? 0 : amount);
      }, 0);

      this.totalIncome = total.toFixed(2);
      this.totalDialogVisible = true;
    },

    openExpenseDialog() {
      this.expenseAmount = 0;
      this.dialogVisible2 = true;
    },
    closeExpenseDialog() {
      this.dialogVisible2 = false;
    },
    async saveExpense() {
      const expenseData = {
        ExpenseType: 'other',
        ExpenseAmount: -Math.abs(this.expenseAmount),
        Date: new Date().toISOString().split('T')[0],
        Order: null
      };

      try {
        const response = await fetch('http://localhost:8000/api/expenses/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(expenseData),
        });

        if (!response.ok) {
          const errorMessage = await response.json();
          throw new Error(errorMessage.error || '费用记录创建失败');
        }

        await this.getExpenses();
        this.closeExpenseDialog();
        this.$message.success('费用记录成功创建');
      } catch (error) {
        console.error('记录费用时出错:', error.message);
        this.$message.error('记录费用时出错，请稍后再试。');
      }
    },

    async openTableDialog(tableID) {
      try {
        const response = await this.$http.get(`http://localhost:8000/api/tables/${tableID}/orders/`);
        this.currentTableOrder = response.data.length > 0 ? response.data[0] : {};
        this.tableDialogVisible = true;
      } catch (error) {
        console.error('获取桌子订单信息失败:', error);
        this.$message.error('获取订单信息失败，请稍后再试。');
      }
    },

    closeTableDialog() {
      this.tableDialogVisible = false;
    },

    goToMenu() {
      this.$router.push({ name: 'Dishes' });
    },
    goToAdmin() {
    window.location.href = 'http://localhost:8000/admin';
    },
    selectType(type) {
      this.currentType = type;
      if (type === 'order') {
        this.getOrders();
      } else if (type === 'table') {
        this.getTables();
      } else if (type === 'material') {
        this.getMaterials();
      } else if (type === 'expense') {
        this.getExpenses();
      }
    },
  },
};
</script>

<style scoped>
.main-container {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    bottom: 10px;
    background-color: #e0f4bf;
    border-radius: 15px;
    padding: 20px;
    box-sizing: border-box;
    height: auto;
}
.header {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    background-color: #9fc886;
    border-radius: 15px;
    padding-left: 40px;
    font-family: 'Vivaldi', sans-serif;
    box-sizing: border-box;
    text-align: left;
    font-size: 40px;
    color: #ffffff;
    font-weight: 600;
}
.aside {
    position: absolute;
    top: 76px;
    left: 10px;
    right: 10px;
    bottom: 10px;
    background-color: #cfe887;
    border-radius: 15px;
    font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
    font-size: 30px;
    padding-top: 10px;
    box-sizing: border-box;
}

.order_container, .table_container, .material_container, .expense_container {
    position: absolute;
    top: 76px;
    left: 220px;
    right: 10px;
    bottom: 10px;
    background-color: #c6e89c;
    padding: 20px;
    box-sizing: border-box;
    border-radius: 15px;
    overflow: auto;
}

.order_list, .table_list, .material_list, .expense_list {
    list-style-type: none;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
}

.order_item, .table_item, .material_item, .expense_item {
    display: flex;
    background-color: white;
    margin: 10px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    flex: 0 1 calc(50% - 20px);
    font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
    font-size: 20px;
}

.order_info, .table_info, .material_info, .expense_info {
    flex: 1;
    background-color: #d5eeb5;
    position: relative;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.order_description, .table_status, .material_quantity, .expense_amount {
    font-size: 14px;
    margin: 10px 0;
}

.menu-item {
  background-color: #cfe887;
  border-radius: 10px;
  margin-bottom: 10px;
  padding: 10px;
  color: black;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-item:hover,
.menu-item.is-active {
  background-color: #bee05c;
}

.el-menu {
  background-color: transparent;
  padding: 10px;
  border: none;
}

.custom-button1 {
  color: #76c02f;
  position: absolute;
  top: 154px;
  right: 20px;
  border: none;
  box-shadow: none;
}

.custom-button2 {
  color: #76c02f;
  position: absolute;
  top: 14px;
  right: 100px;
  border: none;
  box-shadow: none;
}

.custom-button3 {
  color: #76c02f;
  width: 72px;
  position: absolute;
  top: 14px;
  right: 20px;
  border: none;
  box-shadow: none;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
  font-size: 16px;
}

.material_info {
  position: relative;
}

.custom-button4 {
  color: #76c02f;
  position: absolute;
  top: 88px;
  right: 20px;
  border: none;
  box-shadow: none;
}

.table_info {
  position: relative;
}

.custom-button5 {
  color: #76c02f;
  position: absolute;
  top: 56px;
  right: 20px;
  border: none;
  box-shadow: none;
}

.total_button {
  color: #76c02f;
  position: relative;
  top: -4px;
  right: -698px;
  border: none;
  box-shadow: none;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
  font-size: 16px;
}

.add_expense {
  color: #76c02f;
  position: relative;
  top: -4px;
  right: -468px;
  border: none;
  box-shadow: none;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
  font-size: 16px;
}

.custom-dialog {
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
}

.dialog-content {
  text-align: left;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
  font-size: 20px;
}

.separator {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 10px 0;
}

.dish-list {
  list-style-type: none;
  padding: 0;
}

.dish-list li {
  margin: 5px 0;
}

.custom-button6 {
  box-shadow: none;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
  border: 1px solid #76c02f;
}
</style>