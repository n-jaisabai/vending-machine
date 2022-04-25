import Meta from "../components/Meta"
import ProductCard from "../components/Product"
import styles from '../styles/Home.module.css'
import { useEffect, useState } from "react";

import Grid from '@mui/material/Grid';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import CancelIcon from '@mui/icons-material/Cancel';

export default function Home() {
  const [products, setProducts] = useState([]);
  const [coinType, setCoinType] = useState('one_coin');
  const [machine, setMachine] = useState({
    "name": "",
    "one_coin":0,
    "five_coin":0,
    "ten_coin":0,
    "twenty_banknote":0,
    "fifty_banknote":0,
    "hundred_banknote":0,
    "five_hundred_banknote":0,
    "thousand_banknote":0
  });
  const [pendingCoin, setPendingCoin] = useState({
    "one_coin":0,
    "five_coin":0,
    "ten_coin":0,
    "twenty_banknote":0,
    "fifty_banknote":0,
    "hundred_banknote":0,
    "five_hundred_banknote":0,
    "thousand_banknote":0,
    "total":0
  });

  const coinTypeChange = (event) => {
    setCoinType(event.target.value);
  };

  const insertCoin = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/coin`, {
      method: 'PUT',
      body: JSON.stringify( { coin_type: coinType } ),
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const json = await res.json();
    if (res.status === 200) {
      setPendingCoin({
        "one_coin": json?.one_coin,
        "five_coin": json?.five_coin,
        "ten_coin": json?.ten_coin,
        "twenty_banknote": json?.twenty_banknote,
        "fifty_banknote": json?.fifty_banknote,
        "hundred_banknote": json?.hundred_banknote,
        "five_hundred_banknote": json?.five_hundred_banknote,
        "thousand_banknote": json?.thousand_banknote,
        "total": json?.total
      })
    }
  }

  const chooseProduct = async (id) => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/transaction`, {
      method: 'POST',
      body: JSON.stringify( { product_id: id } ),
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const json = await res.json();
    if (res.status === 200) {
      fetchProducts();
      fetchMachine();
      setPendingCoin({
        "one_coin": 0,
        "five_coin": 0,
        "ten_coin": 0,
        "twenty_banknote": 0,
        "fifty_banknote": 0,
        "hundred_banknote": 0,
        "five_hundred_banknote": 0,
        "thousand_banknote": 0,
        "total": 0
      })
    }
  }

  const cancelTransaction = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/transaction/cancel`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const json = await res.json();
    if (res.status === 200) {
      setPendingCoin({
        "one_coin": 0,
        "five_coin": 0,
        "ten_coin": 0,
        "twenty_banknote": 0,
        "fifty_banknote": 0,
        "hundred_banknote": 0,
        "five_hundred_banknote": 0,
        "thousand_banknote": 0,
        "total": 0
      })
    }
  }

  async function fetchMachine() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/machine`);
    const json = await res.json();
    setMachine({
      "name": json?.name,
      "one_coin": json?.one_coin,
      "five_coin": json?.five_coin,
      "ten_coin": json?.ten_coin,
      "twenty_banknote": json?.twenty_banknote,
      "fifty_banknote": json?.fifty_banknote,
      "hundred_banknote": json?.hundred_banknote,
      "five_hundred_banknote": json?.five_hundred_banknote,
      "thousand_banknote": json?.thousand_banknote
    })
  }
  
  async function fetchPendingCoin() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/coin`);
    const json = await res.json();
    setPendingCoin({
      "one_coin": json?.one_coin,
      "five_coin": json?.five_coin,
      "ten_coin": json?.ten_coin,
      "twenty_banknote": json?.twenty_banknote,
      "fifty_banknote": json?.fifty_banknote,
      "hundred_banknote": json?.hundred_banknote,
      "five_hundred_banknote": json?.five_hundred_banknote,
      "thousand_banknote": json?.thousand_banknote,
      "total": json?.total
    })
  }
  
  async function fetchProducts() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/products`);
    const json = await res.json();
    setProducts(json);
  }

  useEffect(() => {
    fetchMachine();
    fetchPendingCoin();
    fetchProducts();
  }, [])
  
  return (
    <div className={styles.container}>
      <Meta/>

      <Grid container spacing={2}>
        <Grid item xs={8} className={styles.overflow}>
          <h2>Products</h2>
          <Grid container spacing={2}>
            {products.map(product => (
              <Grid item xs={12} md={4} lg={3} key={product.id} >
                <ProductCard product={product} chooseProduct={chooseProduct} />
              </Grid>
            ))}
          </Grid>
        </Grid>
        <Grid item xs={4} className={styles.overflow}>
          <h2>Simulator</h2>

          <h4>Insert coin</h4>
          <FormControl sx={{ m: 1, minWidth: '70%' }} size="small">
            <InputLabel id="demo-select-small">Coin type</InputLabel>
            <Select
              labelId="demo-select-small"
              id="demo-select-small"
              value={coinType}
              label="Coin type"
              onChange={coinTypeChange}
            >
              <MenuItem value={'one_coin'}>1 THB</MenuItem>
              <MenuItem value={'five_coin'}>5 THB</MenuItem>
              <MenuItem value={'ten_coin'}>10 THB</MenuItem>
              <MenuItem value={'twenty_banknote'}>20 THB</MenuItem>
              <MenuItem value={'fifty_banknote'}>50 THB</MenuItem>
              <MenuItem value={'hundred_banknote'}>100 THB</MenuItem>
              <MenuItem value={'five_hundred_banknote'}>500 THB</MenuItem>
              <MenuItem value={'thousand_banknote'}>1000 THB</MenuItem>
            </Select>
          </FormControl>
          <FormControl sx={{ m: 1, minWidth: '20%' }} >
          <Button variant="contained" startIcon={<AttachMoneyIcon />} 
            onClick={insertCoin}>
            Insert
          </Button>
          </FormControl>

          <h4>Cancel</h4>
          <FormControl sx={{ m: 1, minWidth: '20%' }} >
          <Button variant="contained" color="error" startIcon={<CancelIcon />} 
            onClick={cancelTransaction}>
            Cancel
          </Button>
          </FormControl>

          <br/>
          <h2>Coin summary</h2>
          <span>Total coins: {pendingCoin.total} THB</span>
          <ul>
            {pendingCoin.one_coin > 0 ? (<li>coins of 1 THB: {pendingCoin.one_coin}</li>) : ''}
            {pendingCoin.five_coin > 0 ? (<li>coins of 5 THB: {pendingCoin.five_coin}</li>) : ''}
            {pendingCoin.ten_coin > 0 ? (<li>coins of 10 THB: {pendingCoin.ten_coin}</li>) : ''}
            {pendingCoin.twenty_banknote > 0 ? (<li>banknotes of 20 THB: {pendingCoin.twenty_banknote}</li>) : ''}
            {pendingCoin.fifty_banknote > 0 ? (<li>banknotes of 50 THB: {pendingCoin.fifty_banknote}</li>) : ''}
            {pendingCoin.hundred_banknote > 0 ? (<li>banknotes of 100 THB: {pendingCoin.hundred_banknote}</li>) : ''}
            {pendingCoin.five_hundred_banknote > 0 ? (<li>banknotes of 500 THB: {pendingCoin.five_hundred_banknote}</li>) : ''}
            {pendingCoin.thousand_banknote > 0 ? (<li>banknotes of 1000 THB: {pendingCoin.thousand_banknote}</li>) : ''}
          </ul>

          <br/>
          <h2>Machine summary</h2>
          <span>Machine name: {machine.name}</span>
          <ul>
            <li>coins of 1 THB: {machine.one_coin}</li>
            <li>coins of 5 THB: {machine.five_coin}</li>
            <li>coins of 10 THB: {machine.ten_coin}</li>
            <li>banknotes of 20 THB: {machine.twenty_banknote}</li>
            <li>banknotes of 50 THB: {machine.fifty_banknote}</li>
            <li>banknotes of 100 THB: {machine.hundred_banknote}</li>
            <li>banknotes of 500 THB: {machine.five_hundred_banknote}</li>
            <li>banknotes of 1000 THB: {machine.thousand_banknote}</li>
          </ul>
        </Grid>
      </Grid>
    </div>
  )
}
