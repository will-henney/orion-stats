program  PDF_2D
  ! calculates the emissivity cube in a given line from the                     
  ! datacubes of density, ionization fraction, temperature                      
  use wfitsutils, only: fitsread, fitswrite, fitsimage 
  ! use emissmod, only: emtype, emissivity 
  implicit none 
  character(len=100)::archivos
  real, dimension(:,:), allocatable :: m0,m1,Vc
  integer, parameter::nbin=220
  integer, dimension(:),allocatable::c
  real, dimension(0:nbin):: bvel
  character(len=15) :: emtype 
  integer ::i,j,k, nx, ny, l, npts
  real, parameter:: valmin= 0.000001 !-999.9 
  real ::  vmax, vmin, dv, sumv, varvc, promvc
  
  print *, 'Emissivity type?' 
  read '(a)', emtype

 ! print*,'filename ', trim(emtype)//'_-040+070.wisomom-sum-xx.fits'
 ! call fitsread(trim(emtype)//'_-040+070.wisomom-sum-xx.fits') 
 ! nx = size(fitsimage, 1) 
 ! ny = size(fitsimage, 2)


 ! allocate( m0(nx, ny) ) 
 ! m0=fitsimage

  print*,'filename ', trim(emtype)//'_-040+070.wisomom-mean-xx.fits'
  call fitsread(trim(emtype)//'_-040+070.wisomom-mean-xx.fits')
  nx = size(fitsimage, 1) 
  ny = size(fitsimage, 2)
  
  allocate(Vc(nx,ny))
  Vc=fitsimage 

  !allocate(Vc(nx,ny))
  !Vc=0.0
  
  allocate(c(nbin))
  c=0                  
 
  deallocate(fitsimage)          ! Free up unneeded memory                    

print*, 'lectura hecha'

  sumv = 0.0
  npts = 0
  do i=1,nx
     do j=1,ny
           sumv = sumv + Vc(i,j)
           npts = npts + 1
       
     end do
  end do
  promvc = sumv/real(npts)
  sumv = 0.0
  npts = 0
  do i=1,nx
     do j=1,ny

           sumv = sumv + (Vc(i,j)-promvc)**2
           npts = npts + 1
       
     end do
  end do
  varvc = sumv/real((npts-1))

  print*,'npts =', npts, 'promvc =', promvc, 'varvc =', varvc                     
 
!vmax=MAXVAL(Vc)
!vmin=1.0e20
!do j=1,ny
!do i=1, nx
!if (Vc(i,j)>valmin) then
!vmin=min(vmin,Vc(i,j))
!end if 
!end do
!end do

vmax=70.0
vmin=-40.0

  print*, 'velocidad maxima', vmax, 'velocidad minima', vmin
 dv=(vmax-vmin)/nbin 
  bvel(0)=vmin  !calculo de bins de velocidad                            
  
  do l=1, nbin
    bvel(l)=bvel(l-1)+ dv
  end do
 
do k=1,nbin

   do i=1,nx
      do j=1,ny
         if(bvel(k-1)<Vc(i,j) .and. Vc(i,j) <=bvel(k))then
         c(k)=c(k)+1
         endif
      end do
   end do
 

end do
 
print*, 'conteo hecho'

archivos=trim(emtype)//'-pdf-vc'//'.dat'
open(10,file=archivos,status="unknown")
do l=0,nbin-1
  
   WRITE(10,*)   (bvel(l)), (c(l+1))
end do
close(10)   

end program PDF_2D

