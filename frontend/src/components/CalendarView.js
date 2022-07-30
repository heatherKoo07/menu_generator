import { Alert, Calendar, Space, Badge, Card } from "antd";
import moment from "moment";
import React, { useState, useEffect } from "react";
import MenuGenerationForm from "./MenuGenerationForm";

const CalendarView = () => {
  const [value, setValue] = useState(moment());
  const [selectedValue, setSelectedValue] = useState(moment());
  const [randomMenu, setRandomMenu] = useState([]);
  const [error, setError] = useState(undefined);

  console.log(randomMenu);
  const onSelect = (newValue) => {
    setValue(newValue);
    setSelectedValue(newValue);
  };

  const onPanelChange = (newValue) => {
    setValue(newValue);
  };

  const getListData = (value) => {
    console.log(value.format("YYYY-MM-DD"));
    const date = value.format("YYYY-MM-DD");
    if (date in randomMenu) {
      return [
        {
          type: "warning",
          content: randomMenu[date]["lunch"],
        },
        {
          type: "success",
          content: randomMenu[date]["dinner"],
        },
      ];
    }
    return [];
  };

  const dateCellRender = (value) => {
    const listData = getListData(value);
    return (
      <ul className="events">
        {listData.map((item) => (
          <li key={item.content}>
            <Badge status={item.type} text={item.content} />
          </li>
        ))}
      </ul>
    );
  };

  return (
    <Card
      title={
        <Space direction="vertical">
          {error ? (
            <Alert message={error} type="error" closable showIcon />
          ) : null}
          <Alert
            message="Changing the deduplication day will generate a different menu"
            type="warning"
            closable
          />
          <MenuGenerationForm
            startDate={selectedValue?.format("YYYY-MM-DD")}
            setRandomMenu={setRandomMenu}
            setError={setError}
          />
        </Space>
      }
    >
      <Calendar
        value={value}
        onSelect={onSelect}
        onPanelChange={onPanelChange}
        dateCellRender={dateCellRender}
      />
    </Card>

    // <Space direction="vertical">
    //   <Alert
    //     message="Changing the deduplication day will generate a different menu"
    //     type="warning"
    //     closable
    //   />
    //   <MenuGenerationForm
    //     startDate={selectedValue?.format("YYYY-MM-DD")}
    //     setRandomMenu={setRandomMenu}
    //   />

    //   <Calendar
    //     value={value}
    //     onSelect={onSelect}
    //     onPanelChange={onPanelChange}
    //     dateCellRender={dateCellRender}
    //   />
    // </Space>
  );
};

export default CalendarView;
