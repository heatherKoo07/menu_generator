import { Space } from "antd";
import "antd/dist/antd.css";
import CalendarView from "./components/CalendarView";
import MenuListView from "./components/MenuListView";
import "./App.css";

const App = () => {
  return (
    <Space direction="vertical">
      <MenuListView />
      <CalendarView />
    </Space>
  );
};

export default App;
