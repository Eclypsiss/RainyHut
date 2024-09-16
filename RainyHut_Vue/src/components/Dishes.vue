<template>
  <div class="common-layout">
    <el-container class="main-container">
      <el-header class="header">
        Menu
        <el-button color="white" :icon="ShoppingCart" circle class="custom-button2" @click="openDrawer"/>
        <el-button color="white" class="custom-button3" round @click="goToAdmin">Manage</el-button>
      </el-header>
      <el-container>
        <el-aside class="aside" width="200px">
          <h5 class="mb-2">分类</h5>
          <el-menu default-active="1" class="el-menu-vertical-demo">
            <el-menu-item index="1" @click="selectType('light_meal')" class="menu-item">简餐</el-menu-item>
            <el-menu-item index="2" @click="selectType('desserts')" class="menu-item">甜品</el-menu-item>
            <el-menu-item index="3" @click="selectType('drinks')" class="menu-item">饮品</el-menu-item>
            <el-menu-item index="4" @click="selectType('the_rest')" class="menu-item">其他</el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <div class="dishes_container">
            <div class="dishes_list">
              <div
                v-for="dish in filteredDishes"
                :key="dish.DishesID"
                class="dish_item">
                <div class="dish_image" :style="{ backgroundImage: `url(${getFullImageUrl(dish.Pictures)})` }"></div>
                <div class="dish_info">
                  <h2>{{ dish.DishesName }}</h2>
                  <p class="dish_description">{{ dish.Description }}</p>
                  <p class="dish_price">价格: ${{ dish.DishesPrice }}</p>
                  <el-button color="white" :icon="Plus" circle class="custom-button1" @click="addToCart(dish)"/>
                </div>
              </div>
            </div>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>

  <el-drawer
    v-model="drawerVisible"
    size="30%"
    :close-on-click-modal="false"
  >
    <div>
      <h3>购物车内容</h3>
      <hr class="divider" />
      <div v-if="cartItems.length === 0" class="empty-cart">
        <p>购物车为空</p>
        <p>请添加一些菜品到购物车中。</p>
      </div>
      <div v-else>
        <ul class="cart-items-list">
          <li v-for="item in cartItems" :key="item.id" class="cart-item">
            <div class="cart-item-image" :style="{ backgroundImage: `url(${getFullImageUrl(item.image)})` }"></div>
            <div class="cart-item-info">
              <p class="cart-item-name">{{ item.name }}</p>
              <p class="cart-item-price">价格: ${{ item.price }}</p>
              <p class="cart-item-quantity">数量: {{ item.quantity }}</p>
            </div>
            <el-button color="white" :icon="Delete" circle class="custom-button4" @click="removeFromCart(item.id)" />
          </li>
        </ul>
        <p class="total-price">总价格: ${{ calculateTotal() }}</p>
      </div>
      <hr class="divider" />

      <div class="order-type">
        <label class="radio-container">
          <input type="radio" name="orderType" value="dine_in" v-model="orderType" />
          堂食
          <span class="checkmark"></span>
        </label>
        <label class="radio-container">
          <input type="radio" name="orderType" value="takeaway" v-model="orderType" />
          外卖
          <span class="checkmark"></span>
        </label>
      </div>

      <div v-if="orderType === 'takeaway'">
        <el-input v-model="address" placeholder="请输入收货地址" class="custom-input"></el-input>
      </div>
      <div v-if="orderType === 'dine_in'">
        <el-select v-model="tableNumber" placeholder="请选择桌号" class="custom-select">
          <el-option v-for="n in 12" :key="n" :label="`桌号 ${n}`" :value="n" class="el-option"></el-option>
        </el-select>
      </div>
      <hr class="divider" />
      <el-button color="#76c02f" @click="checkout"  round class="custom-button5">结算</el-button>
    </div>
  </el-drawer>
</template>

<script>
import {Delete, Plus, ShoppingCart} from '@element-plus/icons-vue';
import axios from "axios";

export default {
  components: {
    Plus,
    ShoppingCart,
  },
  data() {
    return {
      dishes: [],
      selectedType: 'light_meal',
      drawerVisible: false,
      cartItems: [],
      orderType: 'dine_in',
      address: '',
      tableNumber: null
    };
  },
  created() {
    this.getData();
  },

  methods: {
    async getData() {
      try {
        const response = await this.$http.get('http://localhost:8000/api/dishes/');
        this.dishes = response.data;
        console.log(this.dishes);
      } catch (error) {
        console.error("获取菜品数据失败:", error);
      }
    },

    goToAdmin() {
    this.$router.push({ name: 'Admin' });
    },

    selectType(type) {
      this.selectedType = type;
    },

    getFullImageUrl(relativeUrl) {
      console.log("Relative URL:", relativeUrl);
      return `http://localhost:8000${relativeUrl}`;
    },

    openDrawer() {
      this.drawerVisible = true;
    },

    removeFromCart(itemId) {
      const itemIndex = this.cartItems.findIndex(item => item.id === itemId);
      if (itemIndex !== -1) {
        if (this.cartItems[itemIndex].quantity > 1) {
          this.cartItems[itemIndex].quantity -= 1;
        } else {
          this.cartItems.splice(itemIndex, 1);
        }
      }
    },

    addToCart(dish) {
      if (dish.cookable === "no") {
          this.$message({
              type: 'warning',
              message: `${dish.DishesName} 已售罄，无法添加到购物车。`,
              duration: 3000
          });
          return;
      }

      const existingItem = this.cartItems.find(item => item.id === dish.DishesID);

      if (existingItem) {
          existingItem.quantity += 1;
      } else {
          this.cartItems.push({
              id: dish.DishesID,
              name: dish.DishesName,
              price: dish.DishesPrice,
              image: dish.Pictures,
              quantity: 1
          });
      }
    },

    calculateTotal() {
      return this.cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
    },

    checkout() {
      const baseUrl = 'http://localhost:8000';

      if (this.orderType === 'takeaway') {
        const takeawayData = {
          TakeawayAdd: this.address
        };

        axios.post(`${baseUrl}/api/takeaway/`, takeawayData)
          .then(response => {
            const takeawayID = response.data.TakeawayID;

            const orderData = {
              order_type: this.orderType,
              table_id: null,
              takeaway_id: takeawayID,
              total_amount: this.calculateTotal(),
              items: this.cartItems.map(item => ({
                id: item.id,
                quantity: item.quantity
              }))
            };

            return axios.post(`${baseUrl}/api/order/`, orderData);
          })
          .then(response => {
            this.$message({
              type: 'success',
              message: '订单已创建: ' + response.data.OrderID,
            });
            this.cartItems = [];
            this.address = '';
            this.drawerVisible = false;
          })
          .catch(error => {
            console.error('创建订单时发生错误:', error.response ? error.response.data : error.message);
          });
      } else if (this.orderType === 'dine_in') {
        axios.get(`${baseUrl}/api/tables/${this.tableNumber}/status/`)
          .then(response => {
            const tableStatus = response.data.status;

            if (tableStatus === 'in_use') {
              this.$message({
                type: 'error',
                message: '当前餐桌已被占用，请选择其他餐桌！',
              });
              return Promise.reject();
            }

            const orderData = {
              order_type: this.orderType,
              table_id: this.tableNumber,
              takeaway_id: null,
              total_amount: this.calculateTotal(),
              items: this.cartItems.map(item => ({
                id: item.id,
                quantity: item.quantity
              }))
            };

            console.log("要发送的订单数据: ", orderData);

            return axios.post(`${baseUrl}/api/order/`, orderData);
          })
          .then(response => {
            return axios.put(`${baseUrl}/api/tables/${this.tableNumber}/status/`, {
              TableStatus: 'in_use'
            });
          })
          .then(() => {
            this.$message({
              type: 'success',
              message: '订单已创建成功！',
            });
            this.cartItems = [];
            this.drawerVisible = false;
            this.tableNumber = null;
          })
          .catch(error => {
            console.error('创建订单时发生错误:', error.response ? error.response.data : error.message);
          });
      }
    }
  },
  computed: {

    Delete() {
      return Delete
    },

    Plus() {
      return Plus
    },

    ShoppingCart() {
      return ShoppingCart
    },

    filteredDishes() {
      return this.dishes.filter(dish => {
        if (this.selectedType === 'light_meal') {
          return dish.DishesType === 'light_meal';
        } else if (this.selectedType === 'desserts') {
          return dish.DishesType === 'desserts';
        } else if (this.selectedType === 'drinks') {
          return dish.DishesType === 'drinks';
        } else {
          return dish.DishesType === 'the_rest';
        }
      });
    }
  }
}

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
    padding-left: 54px;
    font-family: 'Vivaldi', sans-serif;;
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
    font-family: '字小魂云溪锦书(商用需授权)', sans-serif;;
    font-size: 30px;
    padding-top: 10px;
    box-sizing: border-box;
}
.dishes_container {
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

.dishes_list {
    list-style-type: none;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
}

.dish_item {
    display: flex;
    background-color: white;
    margin: 10px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    flex: 0 1 calc(50% - 20px);
    font-family: '字小魂云溪锦书(商用需授权)', sans-serif;;
    font-size: 20px;
}

.dish_image {
    flex: 1;
    height: 200px;
    background-size: cover;
    background-position: center;
}

.dish_info {
    flex: 1;
    background-color: #d5eeb5;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.dish_description {
    font-size: 14px;
    margin: 10px 0;
}

.dish_price {
    font-weight: bold;
    margin-top: 10px;
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

.dish_info {
  position: relative;
}

.custom-button1 {
  color: #76c02f;
  position: absolute;
  top: 144px;
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
  position: absolute;
  top: 14px;
  right: 20px;
  border: none;
  box-shadow: none;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;;
  font-size: 16px;
}

.custom-button4 {
  color: #76c02f;
  top: 14px;
  right: 100px;
  border: none;
  box-shadow: none;
}

.custom-button5 {
  border: none;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;;
  font-size: 16px;
}

.empty-cart {
  text-align: center;
  padding: 20px;
  border: 1px dashed #e0e0e0;
  border-radius: 5px;
  margin: 10px 0;
  color: #888;
}

.cart-items-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e0e0e0;
}

.cart-item-image {
  width: 60px;
  height: 60px;
  background-size: cover;
  background-position: center;
  margin-right: 10px;
}

.cart-item-info {
  flex-grow: 1;
  text-align: left;
}

.cart-item-name,
.cart-item-price,
.cart-item-quantity {
  margin: 0;
}

.divider {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 10px 0;
}

.total-price {
  text-align: right;
  font-weight: bold;
  margin-top: 10px;
}

.el-drawer {
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;;
}

.el-drawer h3,
.el-drawer p {
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;;
  font-size: 20px;
}
.order-type {
  margin: 16px;
}

.radio-container {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  margin-right: 20px;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;;
  font-size: 20px;
}

.checkmark {
  width: 14px;
  height: 14px;
  border: 1px solid #76c02f;
  border-radius: 50%;
  position: relative;
  margin-right: 1px;
  transition: background-color 0.2s, border-color 0.2s;
  top: 2px;
  left: 4px;
}

.radio-container input:checked + .checkmark::after {
  content: "";
  width: 7px;
  height: 7px;
  background: #76c02f;
  border-radius: 50%;
  position: absolute;
  top: 3px;
  left: 3px;
}

.radio-container input {
  display: none;
}

.el-option {
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;;
}

.custom-input {
  width: 300px;
  font-family: '字小魂云溪锦书(商用需授权)', sans-serif;
  font-size: 16px;
  border-radius: 4px;
}

</style>

