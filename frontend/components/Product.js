import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';

export default function ProductCard({ product, chooseProduct }) {
  
  const chooseProductClick = async () => {
    chooseProduct(product.id)
  }

  return (
    <Card sx={{ maxWidth: 250 }}>
      <CardActionArea onClick={chooseProductClick}>
        <CardMedia
          component="img"
          height="140"
          image="/watercolor-blue.jpg"
          alt=""
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {product.name}
          </Typography>
          {product.stock > 0 ? (
            <Typography variant="body2" color="text.secondary">
              {product.price} THB ({product.stock} pieces available)
            </Typography>)
            : (
            <Typography variant="body2" color="error">
              Sold out
            </Typography>)
          }
        </CardContent>
      </CardActionArea>
    </Card>
  );
}
