import Vue from 'vue'
import {
    Button,
    Input,
    Form,
    FormItem,
    Message,
    Container,
    Aside,
    Main,
    Header,
    Menu,
    Submenu,
    MenuItem,
    Row,
    Col,
    Table,
    TableColumn,
    Dialog,
    Alert,
    Switch,
    Pagination,
} from 'element-ui'
import { Card, Breadcrumb, BreadcrumbItem } from 'element-ui'

Vue.use(Button)
Vue.use(Input)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Container)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Header)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(Card)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Col)
Vue.use(Row)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Dialog)
Vue.use(Switch)
Vue.use(Pagination)

Vue.prototype.$message = Message
Vue.prototype.$confirm = Alert
