import { useEffect, useState } from "react";
import axios from "axios";

type DataType = {
  flavours: string[];
};

function dummy() {
  const [data, setData] = useState<DataType | null>(null);

  const fetchData = async () => {
    try {
      const response = await axios.get("/data/flavours");
      console.log(response.data);
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <h1>Hello World!</h1>
      {data ? (
        <ul>
          {data.flavours.map((flavour, index) => (
            <li key={index}>{flavour}</li>
          ))}
        </ul>
      ) : (
        <p>Loading...</p>
      )}
    </>
  );
}

export default dummy;