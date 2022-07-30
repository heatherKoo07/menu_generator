import axios from "axios";
import { Button, Form, InputNumber, Typography, Space } from "antd";
import React, { useState } from "react";
const { Text } = Typography;

const MenuGenerationForm = ({ startDate, setRandomMenu, setError }) => {
  const [form] = Form.useForm();
  const onFinish = (values) => {
    console.log("Received values from form: ", values);
    // post request
    axios
      .get("/random_menu", {
        params: {
          start_date: startDate,
          length: values.length,
          dedup_days: values.dedup_days,
        },
      })
      .then(function (response) {
        console.log(response);
        setRandomMenu(response.data);
        setError(null);
      })
      .catch(function (error) {
        console.log(error);
        setError(error.response.data.message);
      });
  };
  // TODO add validation
  return (
    <Form
      layout="inline"
      form={form}
      onFinish={onFinish}
      initialValues={{
        length: 7,
        dedup_days: 5,
      }}
    >
      <Space>
        <Text>Generate a menu from</Text>
        <Text mark strong>
          {startDate}
        </Text>
        <Text>for</Text>

        <Form.Item
          name="length"
          noStyle
          rules={[{ type: "number", min: 1, max: 99 }]}
        >
          <InputNumber />
        </Form.Item>
        <Text>days without duplication within past </Text>
        <Form.Item
          name="dedup_days"
          noStyle
          rules={[{ type: "number", min: 0, max: 99 }]}
        >
          <InputNumber />
        </Form.Item>
        <Text>days</Text>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Space>
    </Form>
  );
};

export default MenuGenerationForm;
